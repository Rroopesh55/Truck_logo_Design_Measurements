"""
Truck classification module based on bounding box dimensions
"""

import logging

from .config import (
    TRUCK_HEIGHTS,
    HEIGHT_THRESHOLDS,
    ASPECT_RATIO_THRESHOLDS
)


class TruckClassifier:
    """
    Classifies truck types based on bounding box dimensions
    """
    
    def __init__(self):
        """Initialize the truck classifier"""
        self.truck_heights = TRUCK_HEIGHTS
        self.height_thresholds = HEIGHT_THRESHOLDS
        self.aspect_ratio_thresholds = ASPECT_RATIO_THRESHOLDS
    
    def classify(self, bbox_width, bbox_height):
        """
        Classify truck type based on bounding box dimensions
        
        Args:
            bbox_width (int): Bounding box width in pixels
            bbox_height (int): Bounding box height in pixels
            
        Returns:
            tuple: (truck_type, truck_height_meters)
        """
        aspect_ratio = bbox_width / bbox_height
        
        logging.debug(f"Classification input - Width: {bbox_width}, "
                     f"Height: {bbox_height}, Aspect Ratio: {aspect_ratio:.2f}")
        
        # Classification logic based on size and aspect ratio
        truck_type = self._determine_truck_type(bbox_height, aspect_ratio)
        truck_height = self.truck_heights[truck_type]
        
        logging.info(f"Classified as: {truck_type} (Height: {truck_height}m)")
        
        return truck_type, truck_height
    
    def _determine_truck_type(self, bbox_height, aspect_ratio):
        """
        Determine truck type based on height and aspect ratio
        
        Args:
            bbox_height (int): Bounding box height in pixels
            aspect_ratio (float): Width to height ratio
            
        Returns:
            str: Truck type
        """
        if bbox_height > self.height_thresholds["large"]:
            # Large trucks - distinguish by aspect ratio
            if aspect_ratio > self.aspect_ratio_thresholds["semi_trailer"]:
                return "Semi Trailer"
            else:
                return "Box Truck"
        
        elif bbox_height > self.height_thresholds["medium"]:
            return "Cube Van"
        
        elif bbox_height > self.height_thresholds["small"]:
            return "Sprinter Van"
        
        else:
            return "Cargo Van"
    
    def get_truck_height(self, truck_type):
        """
        Get the standard height for a truck type
        
        Args:
            truck_type (str): Type of truck
            
        Returns:
            float: Height in meters
        """
        return self.truck_heights.get(truck_type, 
                                    self.truck_heights["Unknown Truck"])
    
    def get_all_truck_types(self):
        """
        Get all supported truck types
        
        Returns:
            dict: Dictionary of truck types and their heights
        """
        return self.truck_heights.copy()
    
    def validate_classification(self, truck_type):
        """
        Validate if truck type is supported
        
        Args:
            truck_type (str): Truck type to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return truck_type in self.truck_heights