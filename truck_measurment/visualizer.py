"""
Image visualization module for drawing annotations and measurements
"""

import cv2
import logging

from .config import COLORS, FONT_SETTINGS


class ImageVisualizer:
    """
    Handles all image drawing and visualization operations
    """
    
    def __init__(self):
        """Initialize the image visualizer"""
        self.colors = COLORS
        self.font = FONT_SETTINGS["font"]
        self.font_scale = FONT_SETTINGS["scale"]
        self.font_thickness = FONT_SETTINGS["thickness"]
    
    def draw_truck_detection(self, image, truck_box, truck_type, truck_height):
        """
        Draw truck detection box and label
        
        Args:
            image (numpy.ndarray): Image to draw on
            truck_box (tuple): Truck bounding box (x1, y1, x2, y2)
            truck_type (str): Classified truck type
            truck_height (float): Truck height in meters
        """
        x1, y1, x2, y2 = truck_box
        
        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), self.colors["truck_box"], 2)
        
        # Prepare label text
        label = f'{truck_type} ({truck_height:.2f}m)'
        
        # Draw label with background
        self._draw_text_with_background(image, label, (x1, y1 - 5), 
                                      self.colors["text"], self.colors["background"])
        
        logging.debug(f"Drew truck detection box and label: {label}")
    
    def draw_measurements(self, image, roi, measurements):
        """
        Draw measurement annotations on the image
        
        Args:
            image (numpy.ndarray): Image to draw on
            roi (tuple): Selected region (x, y, width, height)
            measurements (tuple): (width_meters, height_meters)
        """
        x_roi, y_roi, w_roi, h_roi = roi
        roi_width_m, roi_height_m = measurements
        
        # Draw ROI rectangle
        cv2.rectangle(image, (x_roi, y_roi), (x_roi + w_roi, y_roi + h_roi), 
                      self.colors["roi_box"], 2)
        
        # Prepare measurement text
        dimension_text = f"{roi_width_m:.2f}m x {roi_height_m:.2f}m"
        
        # Draw measurement text with background
        self._draw_text_with_background(image, dimension_text, (x_roi, y_roi - 5),
                                      self.colors["text"], self.colors["background"])
        
        logging.debug(f"Drew measurement annotation: {dimension_text}")
    
    def draw_crosshair(self, image, center, size=20, color=None):
        """
        Draw a crosshair at the specified center point
        
        Args:
            image (numpy.ndarray): Image to draw on
            center (tuple): Center point (x, y)
            size (int): Size of crosshair arms
            color (tuple): Color (B, G, R), default is white
        """
        if color is None:
            color = self.colors["text"]
        
        x, y = center
        
        # Horizontal line
        cv2.line(image, (x - size, y), (x + size, y), color, 1)
        
        # Vertical line
        cv2.line(image, (x, y - size), (x, y + size), color, 1)
    
    def draw_grid(self, image, spacing=50, color=None):
        """
        Draw a grid overlay on the image
        
        Args:
            image (numpy.ndarray): Image to draw on
            spacing (int): Grid spacing in pixels
            color (tuple): Grid color (B, G, R)
        """
        if color is None:
            color = (128, 128, 128)  # Gray
        
        height, width = image.shape[:2]
        
        # Vertical lines
        for x in range(0, width, spacing):
            cv2.line(image, (x, 0), (x, height), color, 1)
        
        # Horizontal lines
        for y in range(0, height, spacing):
            cv2.line(image, (0, y), (width, y), color, 1)
    
    def draw_scale_bar(self, image, scale_length_m, pixels_per_meter, position=(50, 50)):
        """
        Draw a scale bar on the image
        
        Args:
            image (numpy.ndarray): Image to draw on
            scale_length_m (float): Length of scale bar in meters
            pixels_per_meter (float): Pixels per meter conversion
            position (tuple): Position of scale bar (x, y)
        """
        x, y = position
        scale_length_pixels = int(scale_length_m * pixels_per_meter)
        
        # Draw scale bar line
        cv2.line(image, (x, y), (x + scale_length_pixels, y), 
                self.colors["text"], 3)
        
        # Draw end markers
        cv2.line(image, (x, y - 5), (x, y + 5), self.colors["text"], 2)
        cv2.line(image, (x + scale_length_pixels, y - 5), 
                (x + scale_length_pixels, y + 5), self.colors["text"], 2)
        
        # Add scale text
        scale_text = f"{scale_length_m:.1f}m"
        self._draw_text_with_background(image, scale_text, 
                                      (x, y - 20), self.colors["text"], 
                                      self.colors["background"])
    
    def _draw_text_with_background(self, image, text, position, text_color, bg_color):
        """
        Draw text with a background rectangle
        
        Args:
            image (numpy.ndarray): Image to draw on
            text (str): Text to draw
            position (tuple): Text position (x, y)
            text_color (tuple): Text color (B, G, R)
            bg_color (tuple): Background color (B, G, R)
        """
        x, y = position
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, self.font, self.font_scale, self.font_thickness
        )
        
        # Draw background rectangle
        padding = 2
        cv2.rectangle(image, 
                      (x - padding, y - text_height - padding), 
                      (x + text_width + padding, y + baseline + padding), 
                      bg_color, -1)
        
        # Draw text
        cv2.putText(image, text, (x, y), self.font, self.font_scale, 
                   text_color, self.font_thickness)
    
    def create_info_panel(self, width=300, height=200):
        """
        Create an information panel for displaying measurement details
        
        Args:
            width (int): Panel width
            height (int): Panel height
            
        Returns:
            numpy.ndarray: Info panel image
        """
        import numpy as np
        
        # Create blank panel
        panel = np.zeros((height, width, 3), dtype=np.uint8)
        panel.fill(50)  # Dark gray background
        
        return panel
    
    def add_info_to_panel(self, panel, info_dict, start_y=20):
        """
        Add information text to an info panel
        
        Args:
            panel (numpy.ndarray): Info panel to draw on
            info_dict (dict): Dictionary of information to display
            start_y (int): Starting Y position for text
        """
        y = start_y
        line_height = 25
        
        for key, value in info_dict.items():
            text = f"{key}: {value}"
            cv2.putText(panel, text, (10, y), self.font, 
                       self.font_scale * 0.8, self.colors["text"], 1)
            y += line_height
    
    def combine_images_horizontal(self, img1, img2, spacing=10):
        """
        Combine two images horizontally with spacing
        
        Args:
            img1 (numpy.ndarray): First image
            img2 (numpy.ndarray): Second image
            spacing (int): Spacing between images
            
        Returns:
            numpy.ndarray: Combined image
        """
        import numpy as np
        
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        # Make heights equal
        max_height = max(h1, h2)
        if h1 < max_height:
            img1 = np.vstack([img1, np.zeros((max_height - h1, w1, 3), dtype=img1.dtype)])
        if h2 < max_height:
            img2 = np.vstack([img2, np.zeros((max_height - h2, w2, 3), dtype=img2.dtype)])
        
        # Create spacing
        spacer = np.zeros((max_height, spacing, 3), dtype=img1.dtype)
        
        # Combine images
        combined = np.hstack([img1, spacer, img2])
        
        return combined