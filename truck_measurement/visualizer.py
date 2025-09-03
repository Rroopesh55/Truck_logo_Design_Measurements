# --- truck_measurement/visualizer.py ---
import cv2


COLORS = {
    "truck_box": (0, 255, 0),      # green
    "roi_box": (0, 255, 255),      # yellow
    "text": (255, 255, 255),       # white
    "bg": (0, 0, 0),               # black
}

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
THICKNESS = 1


class ImageVisualizer:
    def __init__(self):
        self.colors = COLORS

    def draw_truck_detection(self, image, truck_box, truck_type: str, truck_height_m: float):
        x1, y1, x2, y2 = truck_box
        cv2.rectangle(image, (x1, y1), (x2, y2), self.colors["truck_box"], 2)
        label = f"{truck_type} ({truck_height_m:.2f}m)"
        self._text_bg(image, label, (x1, max(15, y1 - 8)))

    def draw_measurements(self, image, roi, measurements):
        x, y, w, h = roi
        width_m, height_m = measurements
        cv2.rectangle(image, (x, y), (x + w, y + h), self.colors["roi_box"], 2)
        self._text_bg(image, f"{width_m:.2f}m x {height_m:.2f}m", (x, max(15, y - 8)))

    def draw_scale_bar(self, image, length_m: float, pixels_per_meter: float, origin=(40, 40)):
        """Draw a horizontal scale bar of given physical length (in meters)."""
        px = int(round(length_m * pixels_per_meter))
        ox, oy = origin
        cv2.line(image, (ox, oy), (ox + px, oy), (255, 255, 255), 2)
        self._text_bg(image, f"{length_m:.1f} m", (ox, oy - 8))

    def draw_grid(self, image, spacing=50):
        h, w = image.shape[:2]
        for x in range(0, w, spacing):
            cv2.line(image, (x, 0), (x, h), (50, 50, 50), 1)
        for y in range(0, h, spacing):
            cv2.line(image, (0, y), (w, y), (50, 50, 50), 1)

    def _text_bg(self, image, text, org):
        (tw, th), base = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)
        x, y = org
        pad = 2
        cv2.rectangle(image, (x - pad, y - th - pad), (x + tw + pad, y + base + pad), self.colors["bg"], -1)
        cv2.putText(image, text, (x, y), FONT, FONT_SCALE, self.colors["text"], THICKNESS, lineType=cv2.LINE_AA)
