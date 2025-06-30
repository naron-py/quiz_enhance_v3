import cv2
import numpy as np
import torch
import re
from pathlib import Path
import logging
from typing import Dict, List, Optional, Union
from PIL import Image
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from concurrent.futures import ThreadPoolExecutor, as_completed

class OCRProcessor:
    def __init__(self):
        """Initialize the OCR processor with docTR"""
        self.logger = logging.getLogger(__name__)
        self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
            self.logger.info("Using GPU for OCR")
        else:
            self.logger.info("Using CPU for OCR")
        self.debug_dir = Path('debug_images')
        self.debug_dir.mkdir(exist_ok=True)
        
    def preprocess_image(self, image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        """Enhanced image preprocessing for better text recognition"""
        try:
            # Convert input to numpy array
            if isinstance(image, str):
                image = Image.open(image).convert('RGB')
                image_np = np.array(image)
            elif isinstance(image, Image.Image):
                image_np = np.array(image)
            else:
                image_np = image

            # Convert to RGB if needed
            if len(image_np.shape) == 2:  # Grayscale
                image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
            elif len(image_np.shape) == 3 and image_np.shape[2] == 4:  # RGBA
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
            elif len(image_np.shape) == 3 and image_np.shape[2] == 3:  # Already RGB
                pass
            else:
                raise ValueError(f"Unexpected image shape: {image_np.shape}")

            # Enhance contrast using CLAHE
            lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            lab = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            return image_np

    def clean_text(self, text: str) -> str:
        """Clean and normalize OCR text output"""
        if not text:
            return ""
            
        # Remove unwanted characters while preserving essential punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\-.,!?\'"]', '', text)
        
        # Fix spacing issues
        text = re.sub(r'(?<![\'\s])([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase
        text = re.sub(r'\s+', ' ', text)  # Fix multiple spaces
        text = re.sub(r'\s*-\s*', '-', text)  # Fix spacing around hyphens
        text = re.sub(r'([.,!?])([^\s])', r'\1 \2', text)  # Fix spacing after punctuation
        
        return text.strip()

    def recognize_text(self, image: Union[str, np.ndarray, Image.Image], min_confidence: float = 0.5) -> str:
        """Perform OCR on the image and return recognized text"""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Perform OCR using docTR
            result = self.model([processed_image])
            
            # Extract text from all blocks
            text_parts = []
            for page in result.pages:
                for block in page.blocks:
                    for line in block.lines:
                        line_text = " ".join(word.value for word in line.words)
                        if line_text.strip():  # Only add non-empty lines
                            text_parts.append(line_text)
            
            # Join and clean the text
            full_text = ' '.join(text_parts)
            cleaned_text = self.clean_text(full_text)
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Error in OCR process: {str(e)}")
            return ""

    def process_quiz_regions(self, regions: Dict[str, np.ndarray]) -> Dict[str, str]:
        """Process multiple quiz regions (question and answers) using batch OCR for maximum GPU speed"""
        # Prepare images in order
        region_names = list(regions.keys())
        images = [self.preprocess_image(regions[name]) for name in region_names]
        results = {}
        try:
            # Batch OCR
            ocr_results = self.model(images)
            for idx, page in enumerate(ocr_results.pages):
                text_parts = []
                for block in page.blocks:
                    for line in block.lines:
                        line_text = " ".join(word.value for word in line.words)
                        if line_text.strip():
                            text_parts.append(line_text)
                full_text = ' '.join(text_parts)
                cleaned_text = self.clean_text(full_text)
                results[region_names[idx]] = cleaned_text
        except Exception as e:
            for name in region_names:
                results[name] = ''
        return results 