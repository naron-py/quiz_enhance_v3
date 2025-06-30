import json
import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ConfigManager:
    """Load and save configuration values from a JSON file."""

    path: str = "config.json"
    data: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.load()

    def default_config(self) -> Dict:
        return {
            'question_region': {'x': 115, 'y': 680, 'width': 680, 'height': 200},
            'answer_regions': {
                'A': {'x': 390, 'y': 880, 'width': 550, 'height': 90},
                'B': {'x': 1040, 'y': 880, 'width': 550, 'height': 90},
                'C': {'x': 390, 'y': 1000, 'width': 550, 'height': 90},
                'D': {'x': 1040, 'y': 1000, 'width': 550, 'height': 90}
            },
            'match_mode': 'Classic',
            'show_processing_times': True,
            'auto_click': True,
            'show_ocr_answer_choices_terminal': True,
            'capture_fullscreen_on_nomatch': True,
            'filter_answer_choice_tags': False,
            'save_all_captured_images': False,
            'active_database': 'default',
            'filter_selected_pattern': True
        }

    def load(self) -> Dict:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = self.default_config()
            self.save()

        # Ensure defaults for any missing fields
        defaults = self.default_config()
        for key, value in defaults.items():
            if key not in self.data:
                self.data[key] = value
        return self.data

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or '.', exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)
