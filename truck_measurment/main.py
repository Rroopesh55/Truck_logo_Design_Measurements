#!/usr/bin/env python3
"""
Main entry point for the Truck Measurement System

This module provides the command-line interface and orchestrates
the measurement process.
"""

import sys
import argparse
import logging
import cv2

from .utils import setup_logging, validate_image_path
from .config import RESIZE_SCALE
from .detector import TruckDetector
from .classifier import TruckClassifier
from .measurement import MeasurementCalculator
from .visualizer import ImageVisualizer


class TruckMeasurementSystem:
    """
    Main system class that orchestrates the measurement process
    """
    
    def __init__(self, resize_scale=RESIZE_SCALE):
        """
        Initialize the measurement system
        
        Args:
            resize_scale (float): Scale factor for image display
        """
        self.resize_scale = resize_scale
        self.detector = TruckDetector()
        self.classifier = TruckClassifier()
        self.calculator = MeasurementCalculator()
        self.visualizer = ImageVisualizer()
    
    def process_image(self, image_path, output_path=None):
        """
        Process a truck image and perform measurements
        
        Args:
            image_path (str): Path to input image
            output_path (str): Optional path to save result
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load and validate image
            image = self._load_image(image_path)
            if image is None:
                return False
            
            # Detect truck
            detection = self._detect_truck(image)
            if detection is None:
                return False
            
            truck_box, confidence = detection
            
            # Classify truck type
            truck_type, truck_height = self._classify_truck(truck_box)
            
            # Visualize detection
            self.visualizer.draw_truck_detection(image, truck_box, 
                                               truck_type, truck_height)
            
            # Get user ROI selection
            roi = self._get_roi_selection(image)
            if roi is None:
                return False
            
            # Calculate measurements
            measurements = self._calculate_measurements(roi, truck_box, truck_height)
            if measurements is None:
                return False
            
            # Visualize measurements
            self.visualizer.draw_measurements(image, roi, measurements)
            
            # Display results
            self._display_results(image, truck_type, measurements, output_path)
            
            return True
            
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return False
    
    def _load_image(self, image_path):
        """Load and resize image"""
        logging.info(f"Loading image: {image_path}")
        image = cv2.imread(image_path)
        
        if image is None:
            logging.error("Failed to load image")
            return None
        
        # Resize for processing
        image = cv2.resize(image, (0, 0), fx=self.resize_scale, fy=self.resize_scale)
        logging.info(f"Image resized to: {image.shape[1]}x{image.shape[0]}")
        
        return image
    
    def _detect_truck(self, image):
        """Detect truck in image"""
        if not self.detector.is_model_loaded():
            logging.error("YOLO model not loaded")
            return None
        
        detections = self.detector.detect_trucks(image)
        if not detections:
            logging.error("No truck detected in the image")
            return None
        
        # Get best detection
        best_detection = self.detector.get_best_detection(detections)
        truck_box = best_detection[:4]  # (x1, y1, x2, y2)
        confidence = best_detection[4]
        
        logging.info(f"Truck detected with confidence: {confidence:.2f}")
        return truck_box, confidence
    
    def _classify_truck(self, truck_box):
        """Classify truck type"""
        x1, y1, x2, y2 = truck_box
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        
        return self.classifier.classify(bbox_width, bbox_height)
    
    def _get_roi_selection(self, image):
        """Get ROI selection from user"""
        logging.info("Waiting for user to select region of interest...")
        roi = cv2.selectROI("Select Logo/Design on Truck", image, 
                           fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Select Logo/Design on Truck")
        
        x, y, w, h = roi
        if w == 0 or h == 0:
            logging.warning("No region selected by user")
            return None
        
        logging.info(f"ROI selected: x={x}, y={y}, width={w}, height={h}")
        return roi
    
    def _calculate_measurements(self, roi, truck_box, truck_height):
        """Calculate real-world measurements"""
        try:
            return self.calculator.calculate(roi, truck_box, truck_height)
        except Exception as e:
            logging.error(f"Error calculating measurements: {e}")
            return None
    
    def _display_results(self, image, truck_type, measurements, output_path):
        """Display final results"""
        roi_width_m, roi_height_m = measurements
        
        # Log results
        logging.info("=" * 50)
        logging.info("MEASUREMENT RESULTS")
        logging.info("=" * 50)
        logging.info(f"Truck Type: {truck_type}")
        logging.info(f"Logo/Design Width: {roi_width_m:.2f} meters")
        logging.info(f"Logo/Design Height: {roi_height_m:.2f} meters")
        logging.info("=" * 50)
        
        # Show image
        cv2.imshow("Truck Measurement Results", image)
        
        # Save if requested
        if output_path:
            cv2.imwrite(output_path, image)
            logging.info(f"Result saved to: {output_path}")
        
        # Wait for user
        logging.info("Press any key to exit...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Truck Logo/Design Measurement System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m truck_measurement image.jpg
  python -m truck_measurement image.jpg --output result.jpg --log-level DEBUG
  python -m truck_measurement image.jpg --log-file measurement.log
        """
    )
    
    parser.add_argument('image_path', help='Path to the truck image file')
    parser.add_argument('--output', '-o', help='Path to save result image')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Set logging level')
    parser.add_argument('--log-file', help='Path to save log messages')
    parser.add_argument('--resize-scale', type=float, default=RESIZE_SCALE,
                       help=f'Image display scale factor (default: {RESIZE_SCALE})')
    parser.add_argument('--version', action='version', 
                       version='Truck Measurement System v1.0')
    
    return parser.parse_args()


def main():
    """Main entry point"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Setup logging
        setup_logging(args.log_level, args.log_file)
        
        # Log startup info
        logging.info("=" * 60)
        logging.info("TRUCK LOGO/DESIGN MEASUREMENT SYSTEM")
        logging.info("=" * 60)
        logging.info(f"Image path: {args.image_path}")
        logging.info(f"Log level: {args.log_level}")
        if args.output:
            logging.info(f"Output path: {args.output}")
        logging.info("=" * 60)
        
        # Validate input
        if not validate_image_path(args.image_path):
            sys.exit(1)
        
        # Initialize system
        system = TruckMeasurementSystem(resize_scale=args.resize_scale)
        
        # Process image
        success = system.process_image(args.image_path, args.output)
        
        if success:
            logging.info("Measurement completed successfully!")
            sys.exit(0)
        else:
            logging.error("Measurement failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()