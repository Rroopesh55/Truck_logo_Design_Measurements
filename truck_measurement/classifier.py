# --- truck_measurement/classifier.py ---
import logging

TRUCK_HEIGHTS = {
    "Semi Trailer": 4.0,
    "Box Truck": 3.5,
    "Cube Van": 3.0,
    "Sprinter Van": 2.5,
    "Cargo Van": 2.0,
}

HEIGHT_THRESHOLDS = {"large": 300, "medium": 200, "small": 100}
ASPECT_RATIO_THRESHOLDS = {"semi_trailer": 2.0}


class TruckClassifier:
    def __init__(self):
        self.truck_heights = TRUCK_HEIGHTS
        self.height_thresholds = HEIGHT_THRESHOLDS
        self.aspect_ratio_thresholds = ASPECT_RATIO_THRESHOLDS

    def classify(self, bbox_width: int, bbox_height: int):
        aspect_ratio = bbox_width / max(1, bbox_height)
        logging.debug(
            f"Classify: w={bbox_width}, h={bbox_height}, AR={aspect_ratio:.2f}"
        )
        truck_type = self._determine_truck_type(bbox_height, aspect_ratio)
        return truck_type, self.truck_heights[truck_type]

    def _determine_truck_type(self, bbox_height: int, aspect_ratio: float) -> str:
        if bbox_height > self.height_thresholds["large"]:
            return (
                "Semi Trailer"
                if aspect_ratio > self.aspect_ratio_thresholds["semi_trailer"]
                else "Box Truck"
            )
        elif bbox_height > self.height_thresholds["medium"]:
            return "Cube Van"
        elif bbox_height > self.height_thresholds["small"]:
            return "Sprinter Van"
        else:
            return "Cargo Van"
