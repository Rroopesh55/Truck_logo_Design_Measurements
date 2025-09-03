"""
Truck Measurement System
"""

__version__ = "1.0.0"
__author__ = "Rroopesh Hari"
__email__ = "rroopesh.hari@okstate.edu"
__description__ = "Computer vision system for measuring objects on trucks"

from .detector import TruckDetector
from .classifier import TruckClassifier
from .measurement import MeasurementCalculator
from .visualizer import ImageVisualizer

__all__ = [
    "TruckDetector",
    "TruckClassifier",
    "MeasurementCalculator",
    "ImageVisualizer",
]
