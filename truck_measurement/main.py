# --- truck_measurement/main.py ---
import argparse
import logging
import os
import cv2

from .utils import setup_logging, validate_image_path
from .detector import TruckDetector
from .classifier import TruckClassifier
from .measurement import MeasurementCalculator
from .visualizer import ImageVisualizer


def process_image(input_path: str, output_path: str | None = None, resize_scale: float = 1.0) -> bool:
    """End-to-end CLI processing: detect → classify → measure → visualize."""
    if not validate_image_path(input_path):
        return False

    img = cv2.imread(input_path)
    if img is None:
        logging.error(f"Failed to read image: {input_path}")
        return False

    if resize_scale and resize_scale != 1.0:
        img = cv2.resize(img, (0, 0), fx=resize_scale, fy=resize_scale)

    detector = TruckDetector()
    classifier = TruckClassifier()
    measurer = MeasurementCalculator()
    viz = ImageVisualizer()

    logging.info("Running detection...")
    detections = detector.detect_trucks(img)
    best = detector.get_best_detection(detections)

    if not best:
        logging.warning("No truck detected.")
        return False

    x1, y1, x2, y2, conf = best
    bbox_w, bbox_h = max(1, x2 - x1), max(1, y2 - y1)

    truck_type, truck_height_m = classifier.classify(bbox_w, bbox_h)

    # Simple demo: measure the same truck bbox as ROI
    roi = (x1, y1, bbox_w, bbox_h)
    width_m, height_m = measurer.calculate(roi, (x1, y1, x2, y2), truck_height_m)

    # Draw overlays
    out = img.copy()
    viz.draw_truck_detection(out, (x1, y1, x2, y2), truck_type, truck_height_m)
    viz.draw_measurements(out, roi, (width_m, height_m))

    # Optional: draw a 1m scale bar
    pixels_per_meter = bbox_h / max(0.001, truck_height_m)
    viz.draw_scale_bar(out, 1.0, pixels_per_meter, (50, 50))

    logging.info(f"Detection: {truck_type}  conf={conf:.2f}  size≈ {width_m:.2f}m x {height_m:.2f}m")

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        cv2.imwrite(output_path, out)
        logging.info(f"Saved result to: {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Truck Measurement CLI")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("-o", "--output", help="Path to save annotated image (optional)")
    parser.add_argument("--scale", type=float, default=1.0, help="Resize factor (e.g. 0.6)")
    parser.add_argument("--log", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args()

    setup_logging(args.log)
    ok = process_image(args.image, args.output, args.scale)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
