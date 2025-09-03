"""
Truck Measurement System

A computer vision application using OpenCV and YOLO that automatically detects trucks in images 
and allows users to measure logos, designs, or other objects on the truck 
surface using real-world dimensions.
"""

__version__ = "1.0.0"
__author__ = "Rroopesh Hari"
__email__ = "rroopesh.hari@okstate.edu"
__description__ = "Computer vision system for measuring objects on trucks"

from .main import TruckMeasurementSystem, main
from .detector import TruckDetector
from .classifier import TruckClassifier
from .measurement import MeasurementCalculator
from .visualizer import ImageVisualizer

__all__ = [
    'TruckMeasurementSystem',
    'TruckDetector', 
    'TruckClassifier',
    'MeasurementCalculator',
    'ImageVisualizer',
    'main'
]