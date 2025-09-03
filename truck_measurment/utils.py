"""
Utility functions for the Truck Measurement System
"""

import os
import sys
import logging
from pathlib import Path
import requests
from urllib.error import URLError

from .config import (
    SUPPORTED_IMAGE_FORMATS, 
    DOWNLOAD_TIMEOUT, 
    DOWNLOAD_CHUNK_SIZE,
    LOG_FORMAT,
    LOG_DATE_FORMAT
)


def setup_logging(log_level="INFO", log_file=None):
    """
    Setup logging configuration
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file (str): Optional log file path
        
    Returns:
        logging.Logger: Configured logger
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def validate_image_path(image_path):
    """
    Validate if the image path exists and is a valid image file
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.exists(image_path):
        logging.error(f"Image file not found: {image_path}")
        return False
    
    # Check file extension
    file_extension = Path(image_path).suffix.lower()
    
    if file_extension not in SUPPORTED_IMAGE_FORMATS:
        logging.error(f"Invalid image format: {file_extension}")
        logging.info(f"Supported formats: {', '.join(SUPPORTED_IMAGE_FORMATS)}")
        return False
    
    return True


def download_file(url, local_path, show_progress=True):
    """
    Download a file from URL with progress tracking
    
    Args:
        url (str): URL to download from
        local_path (str): Local path to save the file
        show_progress (bool): Whether to show download progress
        
    Returns:
        bool: True if successful, False otherwise
    """
    if os.path.exists(local_path):
        logging.info(f"File already exists: {local_path}")
        return True
    
    logging.info(f"Downloading from {url}")
    try:
        response = requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if show_progress and total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"\rDownloading: {progress:.1f}%", end="", flush=True)
        
        if show_progress:
            print()  # New line after progress
            
        logging.info(f"File downloaded successfully: {local_path}")
        return True
        
    except (requests.RequestException, URLError, IOError) as e:
        logging.error(f"Failed to download file: {e}")
        if os.path.exists(local_path):
            os.remove(local_path)  # Clean up partial download
        return False


def ensure_directory(directory_path):
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {directory_path}: {e}")
        return False


def format_measurement(value, unit="m", decimal_places=2):
    """
    Format measurement value for display
    
    Args:
        value (float): Measurement value
        unit (str): Unit of measurement
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted measurement string
    """
    return f"{value:.{decimal_places}f}{unit}"


def validate_roi(roi):
    """
    Validate region of interest selection
    
    Args:
        roi (tuple): Region of interest (x, y, width, height)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if roi is None:
        return False
    
    x, y, w, h = roi
    return w > 0 and h > 0