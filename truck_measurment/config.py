"""
Configuration settings for the Truck Measurement System
"""

# =============================================================================
# IMAGE PROCESSING SETTINGS
# =============================================================================

RESIZE_SCALE = 0.6  # Scale factor for display (0.1-1.0)
DISPLAY_WINDOW_NAME = "Truck Measurement System"

# =============================================================================
# YOLO MODEL SETTINGS
# =============================================================================

YOLO_MODEL_NAME = "yolov5s.pt"
YOLO_MODEL_URL = "https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt"
TRUCK_CLASS_ID = 7  # COCO class ID for 'truck'

# =============================================================================
# TRUCK CLASSIFICATION
# =============================================================================

# Real-world truck heights in meters (based on industry standards)
TRUCK_HEIGHTS = {
    "Semi Trailer": 4.11,
    "Box Truck": 3.96,
    "Cube Van": 2.90,
    "Sprinter Van": 2.74,
    "Cargo Van": 2.44,
    "Unknown Truck": 3.5,  # Default fallback
}

# Classification thresholds (pixels)
HEIGHT_THRESHOLDS = {
    "large": 200,    # Semi Trailer / Box Truck
    "medium": 150,   # Cube Van
    "small": 120,    # Sprinter Van
}

# Aspect ratio thresholds for truck classification
ASPECT_RATIO_THRESHOLDS = {
    "semi_trailer": 2.5,
    "box_truck": 1.5,
}

# =============================================================================
# VISUAL SETTINGS
# =============================================================================

COLORS = {
    "truck_box": (0, 255, 0),      # Green for truck detection
    "roi_box": (0, 0, 255),        # Red for selected region
    "text": (255, 255, 255),       # White text
    "background": (0, 0, 0),       # Black background for text
}

FONT_SETTINGS = {
    "font": 0,  # cv2.FONT_HERSHEY_SIMPLEX
    "scale": 0.6,
    "thickness": 2,
}

# =============================================================================
# LOGGING SETTINGS
# =============================================================================

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# =============================================================================
# FILE VALIDATION
# =============================================================================

SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

# =============================================================================
# NETWORK SETTINGS
# =============================================================================

DOWNLOAD_TIMEOUT = 30  # seconds
DOWNLOAD_CHUNK_SIZE = 8192  # bytes