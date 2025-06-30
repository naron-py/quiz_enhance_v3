# Quiz Enhance v3

This project captures quiz questions from the screen, performs OCR using docTR and attempts to automatically match the correct answer.

## Setup

1. Create and activate a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
   For GPU support install PyTorch with CUDA using the command referenced in `requirements.txt` comments.

## Usage

Start the interactive assistant:
```bash
python terminal_app.py
```

A small CLI is also available:
```bash
python cli.py capture   # capture once
python cli.py config    # show configuration
```

Configuration is stored in `config.json`. Edit it manually or use commands in the interactive shell.

