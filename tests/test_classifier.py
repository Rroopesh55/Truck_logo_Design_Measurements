"""
Unit tests for the truck classifier module
"""

import unittest
from truck_measurement.classifier import TruckClassifier


class TestTruckClassifier(unittest.TestCase):
    """Test cases for TruckClassifier class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.classifier = TruckClassifier()
    
    def test_classify_semi_trailer(self):
        """Test classification of semi trailer"""
        # Large height with high aspect ratio
        truck_type, height = self.classifier.classify(500, 180)  # AR = 2.78
        
        self.assertEqual(truck_type, "Semi Trailer")
        self.assertEqual(height, 4.11)
    
    def test_classify_box_truck(self):
        """Test classification of box truck"""
        # Large height with moderate aspect ratio
        truck_type, height = self.classifier.classify(300, 220)  # AR = 1.36
        
        self.assertEqual(truck_type, "Box Truck")
        self.assertEqual(height, 3.96)
    
    def test_classify_cube_van(self):
        """Test classification of cube van"""
        # Medium height
        truck_type, height = self.classifier.classify(200, 170)
        
        self.assertEqual(truck_type, "Cube Van")
        self.assertEqual(height, 2.90)
    
    def test_classify_sprinter_van(self):
        """Test classification of sprinter van"""
        # Small-medium height
        truck_type, height = self.classifier.classify(180, 130)
        
        self.assertEqual(truck_type, "Sprinter Van")
        self.assertEqual(height, 2.74)
    
    def test_classify_cargo_van(self):
        """Test classification of cargo van"""
        # Small height
        truck_type, height = self.classifier.classify(150, 100)
        
        self.assertEqual(truck_type, "Cargo Van")
        self.assertEqual(height, 2.44)
    
    def test_aspect_ratio_calculation(self):
        """Test aspect ratio calculations in classification"""
        # Test borderline cases
        
        # Just above semi trailer threshold (2.5)
        truck_type, _ = self.classifier.classify(251, 100)  # AR = 2.51
        self.assertIn("Trailer", truck_type)
        
        # Just below semi trailer threshold
        truck_type, _ = self.classifier.classify(249, 100)  # AR = 2.49
        self.assertNotIn("Trailer", truck_type)
    
    def test_get_truck_height(self):
        """Test getting truck height for specific type"""
        height = self.classifier.get_truck_height("Box Truck")
        self.assertEqual(height, 3.96)
        
        # Test unknown type
        height = self.classifier.get_truck_height("Unknown Type")
        self.assertEqual(height, 3.5)  # Default fallback
    
    def test_get_all_truck_types(self):
        """Test getting all supported truck types"""
        truck_types = self.classifier.get_all_truck_types()
        
        # Check if all expected types are present
        expected_types = ["Semi Trailer", "Box Truck", "Cube Van", 
                         "Sprinter Van", "Cargo Van", "Unknown Truck"]
        
        for truck_type in expected_types:
            self.assertIn(truck_type, truck_types)
        
        # Check if heights are reasonable
        for height in truck_types.values():
            self.assertGreater(height, 2.0)
            self.assertLess(height, 5.0)
    
    def test_validate_classification(self):
        """Test classification validation"""
        # Valid truck types
        self.assertTrue(self.classifier.validate_classification("Box Truck"))
        self.assertTrue(self.classifier.validate_classification("Semi Trailer"))
        
        # Invalid truck type
        self.assertFalse(self.classifier.validate_classification("Flying Car"))
    
    def test_edge_cases(self):
        """Test edge cases for classification"""
        # Very small dimensions
        truck_type, height = self.classifier.classify(50, 30)
        self.assertEqual(truck_type, "Cargo Van")
        
        # Very large dimensions
        truck_type, height = self.classifier.classify(1000, 300)
        self.assertEqual(truck_type, "Semi Trailer")
        
        # Square aspect ratio
        truck_type, height = self.classifier.classify(200, 200)
        self.assertEqual(truck_type, "Box Truck")  # Large height, AR = 1.0


if __name__ == '__main__':
    unittest.main()