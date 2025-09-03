# --- truck_measurement/measurement.py ---
import logging


class MeasurementCalculator:
    def __init__(self):
        pass

    def calculate(self, roi, truck_box, truck_height_m):
        """
        roi: (x, y, w, h)
        truck_box: (x1, y1, x2, y2)
        truck_height_m: known real-world height of the truck (meters)
        """
        try:
            x, y, w, h = roi
            x1, y1, x2, y2 = truck_box

            truck_px_h = max(1, y2 - y1)
            scale_m_per_px = truck_height_m / truck_px_h

            width_m = w * scale_m_per_px
            height_m = h * scale_m_per_px

            logging.debug(
                f"Scale: {scale_m_per_px:.6f} m/px (truck_px_h={truck_px_h}, truck_h={truck_height_m})"
            )
            logging.info(f"Measured: {width_m:.2f}m x {height_m:.2f}m")
            return width_m, height_m
        except Exception as e:
            logging.error(f"Measurement error: {e}")
            raise

    def calculate_scale(self, reference_pixels: float, reference_meters: float) -> float:
        if reference_pixels <= 0 or reference_meters <= 0:
            raise ValueError("Reference dimensions must be positive")
        return reference_meters / reference_pixels

    def pixel_to_meters(self, pixel_value: float, scale_m_per_px: float) -> float:
        return pixel_value * scale_m_per_px

    def meters_to_pixels(self, meter_value: float, scale_m_per_px: float) -> float:
        if scale_m_per_px <= 0:
            raise ValueError("Scale factor must be positive")
        return meter_value / scale_m_per_px

    def calculate_area(self, width_m: float, height_m: float) -> float:
        return width_m * height_m

    def validate_measurements(self, measurements, max_reasonable_size=10.0) -> bool:
        w, h = measurements
        if w <= 0 or h <= 0:
            return False
        if w > max_reasonable_size or h > max_reasonable_size:
            return False
        return True
