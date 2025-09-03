"""
Unit tests for the truck detector module
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock

from truck_measurement.detector import TruckDetector


class TestTruckDetector(unittest.TestCase):
    """Test cases for TruckDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = TruckDetector()
    
    @patch('truck_measurement.detector.download_file')
    @patch('truck_measurement.detector.YOLO')
    def test_init_with_successful_model_load(self, mock_yolo, mock_download):
        """Test successful initialization with model loading"""
        mock_download.return_value = True
        mock_model = Mock()
        mock_yolo.return_value = mock_model
        
        detector = TruckDetector()
        
        self.assertIsNotNone(detector.model)
        mock_download.assert_called_once()
        mock_yolo.assert_called_once()
    
    @patch('truck_measurement.detector.download_file')
    def test_init_with_failed_download(self, mock_download):
        """Test initialization with failed model download"""
        mock_download.return_value = False
        
        detector = TruckDetector()
        
        self.assertIsNone(detector.model)
    
    def test_detect_trucks_without_model(self):
        """Test truck detection without loaded model"""
        self.detector.model = None
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        result = self.detector.detect_trucks(image)
        
        self.assertEqual(result, [])
    
    def test_detect_trucks_with_detections(self):
        """Test truck detection with successful detections"""
        # Mock model and results
        mock_model = Mock()
        mock_results = Mock()
        mock_boxes = Mock()
        
        # Mock detection data: [x1, y1, x2, y2, conf, cls]
        detection_data = np.array([
            [10, 20, 100, 120, 0.9, 7],  # truck
            [200, 50, 300, 150, 0.8, 2], # car
            [400, 100, 500, 200, 0.85, 7] # another truck
        ])
        
        mock_boxes.data.cpu.return_value.numpy.return_value = detection_data
        mock_results.boxes = mock_boxes
        mock_model.return_value = [mock_results]
        
        self.detector.model = mock_model
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        result = self.detector.detect_trucks(image)
        
        # Should return 2 truck detections (class 7)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (10, 20, 100, 120, 0.9))
        self.assertEqual(result[1], (400, 100, 500, 200, 0.85))
    
    def test_detect_trucks_no_trucks_found(self):
        """Test truck detection with no trucks in image"""
        mock_model = Mock()
        mock_results = Mock()
        mock_boxes = Mock()
        
        # Mock detection data with no trucks (class 7)
        detection_data = np.array([
            [10, 20, 100, 120, 0.9, 2],  # car
            [200, 50, 300, 150, 0.8, 1], # person
        ])
        
        mock_boxes.data.cpu.return_value.numpy.return_value = detection_data
        mock_results.boxes = mock_boxes
        mock_model.return_value = [mock_results]
        
        self.detector.model = mock_model
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        result = self.detector.detect_trucks(image)
        
        self.assertEqual(len(result), 0)
    
    def test_get_best_detection(self):
        """Test getting the best detection with highest confidence"""
        detections = [
            (10, 20, 100, 120, 0.7),
            (200, 50, 300, 150, 0.9),
            (400, 100, 500, 200, 0.8)
        ]
        
        best = self.detector.get_best_detection(detections)
        
        # Should return detection with confidence 0.9
        self.assertEqual(best, (200, 50, 300, 150, 0.9))
    
    def test_get_best_detection_empty_list(self):
        """Test getting best detection from empty list"""
        result = self.detector.get_best_detection([])
        
        self.assertIsNone(result)
    
    def test_is_model_loaded_true(self):
        """Test is_model_loaded returns True when model is loaded"""
        self.detector.model = Mock()
        
        self.assertTrue(self.detector.is_model_loaded())
    
    def test_is_model_loaded_false(self):
        """Test is_model_loaded returns False when model is None"""
        self.detector.model = None
        
        self.assertFalse(self.detector.is_model_loaded())
    
    def test_detect_trucks_exception_handling(self):
        """Test exception handling in detect_trucks method"""
        mock_model = Mock()
        mock_model.side_effect = Exception("Model error")
        
        self.detector.model = mock_model
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        result = self.detector.detect_trucks(image)
        
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()