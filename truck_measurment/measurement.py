"""
Measurement calculation module for converting pixel measurements to real-world dimensions
"""

import logging


class MeasurementCalculator:
    """
    Calculates real-world measurements from pixel dimensions
    """
    
    def __init__(self):
        """Initialize the measurement calculator"""
        pass
    
    def calculate(self, roi, truck_box, truck_height_m):
        """
        Calculate real-world measurements of the selected region
        
        Args:
            roi (tuple): Selected region (x, y, width, height)
            truck_box (tuple): Truck bounding box (x1, y1, x2, y2)
            truck_height_m (float): Truck height in meters
            
        Returns:
            tuple: (width_meters, height_meters)
        """
        try:
            x_roi, y_roi, w_roi, h_roi = roi
            x1, y1, x2, y2 = truck_box
            
            # Calculate scale factor
            truck_pixel_height = y2 - y1
            scale = truck_height_m / truck_pixel_height
            
            logging.debug(f"Scale calculation - Truck pixel height: {truck_pixel_height}, "
                         f"Real height: {truck_height_m}m, Scale: {scale:.6f}m/pixel")
            
            # Convert to real-world measurements
            roi_width_m = w_roi * scale
            roi_height_m = h_roi * scale
            
            logging.info(f"Measurements calculated - Width: {roi_width_m:.2f}m, "
                        f"Height: {roi_height_m:.2f}m")
            
            return roi_width_m, roi_height_m
            
        except Exception as e:
            logging.error(f"Error calculating measurements: {e}")
            raise
    
    def calculate_scale(self, reference_pixels, reference_meters):
        """
        Calculate pixels per meter scale factor
        
        Args:
            reference_pixels (float): Reference length in pixels
            reference_meters (float): Reference length in meters
            
        Returns:
            float: Scale factor (meters per pixel)
        """
        if reference_pixels <= 0 or reference_meters <= 0:
            raise ValueError("Reference dimensions must be positive")
        
        scale = reference_meters / reference_pixels
        logging.debug(f"Scale factor calculated: {scale:.6f} m/pixel")
        
        return scale
    
    def pixel_to_meters(self, pixel_value, scale):
        """
        Convert pixel measurement to meters
        
        Args:
            pixel_value (float): Value in pixels
            scale (float): Scale factor (meters per pixel)
            
        Returns:
            float: Value in meters
        """
        return pixel_value * scale
    
    def meters_to_pixels(self, meter_value, scale):
        """
        Convert meter measurement to pixels
        
        Args:
            meter_value (float): Value in meters
            scale (float): Scale factor (meters per pixel)
            
        Returns:
            float: Value in pixels
        """
        if scale <= 0:
            raise ValueError("Scale factor must be positive")
        
        return meter_value / scale
    
    def calculate_area(self, width_m, height_m):
        """
        Calculate area in square meters
        
        Args:
            width_m (float): Width in meters
            height_m (float): Height in meters
            
        Returns:
            float: Area in square meters
        """
        return width_m * height_m
    
    def validate_measurements(self, measurements, max_reasonable_size=10.0):
        """
        Validate that measurements are reasonable
        
        Args:
            measurements (tuple): (width_meters, height_meters)
            max_reasonable_size (float): Maximum reasonable size in meters
            
        Returns:
            bool: True if measurements seem reasonable
        """
        width_m, height_m = measurements
        
        if width_m <= 0 or height_m <= 0:
            logging.warning("Measurements must be positive")
            return False
        
        if width_m > max_reasonable_size or height_m > max_reasonable_size:
            logging.warning(f"Measurements seem unreasonably large: {width_m:.2f}m x {height_m:.2f}m")
            return False
        
        return True