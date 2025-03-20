import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

# List of required files
list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trial.ipynb"
]

# Ensure each file exists
for filepath in list_of_files:
    path = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    # Create parent directories if they don't exist
    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file: {filename}")

    # Create the file if it doesn't exist or is empty
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass  # Create an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info("All required files and directories are verified!")
