"""
YOLO-based truck detection module
"""

import logging
from ultralytics import YOLO

from .config import YOLO_MODEL_NAME, YOLO_MODEL_URL, TRUCK_CLASS_ID
from .utils import download_file


class TruckDetector:
    """
    YOLO-based truck detection class
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the truck detector
        
        Args:
            model_path (str): Path to YOLO model file
        """
        self.model_path = model_path or YOLO_MODEL_NAME
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load YOLO model with error handling"""
        try:
            # Download model if it doesn't exist
            if not self._ensure_model_available():
                raise Exception("Failed to download YOLO model")
            
            logging.info(f"Loading YOLO model: {self.model_path}")
            self.model = YOLO(self.model_path)
            logging.info("YOLO model loaded successfully")
            
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            self.model = None
    
    def _ensure_model_available(self):
        """
        Ensure YOLO model is available, download if necessary
        
        Returns:
            bool: True if model is available, False otherwise
        """
        return download_file(YOLO_MODEL_URL, self.model_path)
    
    def detect_trucks(self, image):
        """
        Detect trucks in the given image
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            list: List of truck detections [(x1, y1, x2, y2, confidence), ...]
        """
        if self.model is None:
            logging.error("YOLO model not loaded")
            return []
        
        try:
            logging.info("Running truck detection...")
            results = self.model(image)
            detections = results[0].boxes.data.cpu().numpy()
            
            truck_detections = []
            for det in detections:
                x1, y1, x2, y2, conf, cls = det
                
                # Filter for truck class
                if int(cls) == TRUCK_CLASS_ID:
                    # Convert to integers
                    bbox = (int(x1), int(y1), int(x2), int(y2))
                    truck_detections.append((*bbox, float(conf)))
            
            logging.info(f"Found {len(truck_detections)} truck(s)")
            return truck_detections
            
        except Exception as e:
            logging.error(f"Error during truck detection: {e}")
            return []
    
    def get_best_detection(self, detections):
        """
        Get the truck detection with highest confidence
        
        Args:
            detections (list): List of truck detections
            
        Returns:
            tuple: Best detection (x1, y1, x2, y2, confidence) or None
        """
        if not detections:
            return None
        
        # Sort by confidence (highest first)
        best_detection = max(detections, key=lambda x: x[4])
        logging.info(f"Best truck detection confidence: {best_detection[4]:.2f}")
        
        return best_detection
    
    def is_model_loaded(self):
        """
        Check if YOLO model is loaded
        
        Returns:
            bool: True if model is loaded, False otherwise
        """
        return self.model is not None