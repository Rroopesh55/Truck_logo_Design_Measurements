# --- truck_measurement/detector.py ---
import logging
from typing import List, Tuple

import numpy as np
from ultralytics import YOLO

TRUCK_CLASS_ID = 7  # COCO index for "truck"


class TruckDetector:
    """YOLO-based truck detector."""

    def __init__(self, model_path: str | None = None):
        # Ultralytics will auto-download weights like "yolov8n.pt" if not present
        self.model_path = model_path or "yolov8m.pt"
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            logging.info(f"Loading YOLO model: {self.model_path}")
            self.model = YOLO(self.model_path)
            logging.info("YOLO model loaded.")
        except Exception as e:
            logging.error(f"Failed to load YOLO model: {e}")
            self.model = None

    def is_model_loaded(self) -> bool:
        return self.model is not None

    def detect_trucks(self, image) -> List[Tuple[int, int, int, int, float]]:
        """Returns list of (x1, y1, x2, y2, confidence) for truck detections."""
        if self.model is None:
            logging.error("Model not loaded.")
            return []

        try:
            results = self.model(image)
            if not results or not hasattr(results[0], "boxes") or results[0].boxes is None:
                return []

            boxes = results[0].boxes.data.cpu().numpy()  # [x1,y1,x2,y2,conf,cls]
            out: List[Tuple[int, int, int, int, float]] = []
            for row in boxes:
                x1, y1, x2, y2, conf, cls = row
                if int(cls) == TRUCK_CLASS_ID:
                    out.append((int(x1), int(y1), int(x2), int(y2), float(conf)))
            logging.info(f"Found {len(out)} truck(s).")
            return out
        except Exception as e:
            logging.error(f"Error during detection: {e}")
            return []

    @staticmethod
    def get_best_detection(detections: List[Tuple[int, int, int, int, float]]):
        if not detections:
            return None
        return max(detections, key=lambda d: d[4])
