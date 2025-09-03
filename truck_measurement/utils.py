# --- truck_measurement/utils.py ---
import os
import sys
import logging
from pathlib import Path

SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level="INFO", log_file=None):
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def validate_image_path(image_path: str) -> bool:
    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return False
    ext = Path(image_path).suffix.lower()
    if ext not in SUPPORTED_IMAGE_FORMATS:
        logging.error(f"Unsupported image format: {ext}")
        return False
    return True


def validate_roi(roi) -> bool:
    if roi is None:
        return False
    x, y, w, h = roi
    return w > 0 and h > 0
