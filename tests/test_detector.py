import unittest
import numpy as np
from unittest.mock import Mock
from truck_measurement import TruckDetector  # via __init__.py

class TestTruckDetector(unittest.TestCase):
    def setUp(self):
        # Avoid heavy model load in unit tests if desired:
        self.detector = TruckDetector()
        # Optionally stub the model for speed in real runs:
        # self.detector.model = Mock()

    def test_get_best_detection(self):
        detections = [
            (10, 20, 100, 120, 0.7),
            (200, 50, 300, 150, 0.9),
            (400, 100, 500, 200, 0.8),
        ]
        best = self.detector.get_best_detection(detections)
        self.assertEqual(best, (200, 50, 300, 150, 0.9))

    def test_get_best_detection_empty(self):
        best = self.detector.get_best_detection([])
        self.assertIsNone(best)

    def test_is_model_loaded_flag(self):
        self.detector.model = Mock()
        self.assertTrue(self.detector.is_model_loaded())
        self.detector.model = None
        self.assertFalse(self.detector.is_model_loaded())

    def test_detect_trucks_mocked(self):
        # Mock a YOLO-like result
        mock_model = Mock()
        mock_results = Mock()
        mock_boxes = Mock()
        mock_boxes.data.cpu.return_value.numpy.return_value = np.array([
            [10, 20, 100, 120, 0.9, 7],  # truck
            [200, 50, 300, 150, 0.8, 2], # not truck
            [400, 100, 500, 200, 0.85, 7]# truck
        ])
        mock_results.boxes = mock_boxes
        mock_model.return_value = [mock_results]

        self.detector.model = mock_model
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        trucks = self.detector.detect_trucks(dummy_image)

        self.assertEqual(len(trucks), 2)
        self.assertAlmostEqual(trucks[0][4], 0.9, places=6)
        self.assertAlmostEqual(trucks[1][4], 0.85, places=6)
