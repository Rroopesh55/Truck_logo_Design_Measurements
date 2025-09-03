"""
Unit tests for the measurement calculator module
"""

import unittest
from truck_measurement.measurement import MeasurementCalculator


class TestMeasurementCalculator(unittest.TestCase):
    """Test cases for MeasurementCalculator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = MeasurementCalculator()
    
    def test_calculate_basic(self):
        """Test basic measurement calculation"""
        # ROI: 100x50 pixels
        # Truck box: height of 200 pixels = 4.0 meters
        # Scale: 4.0/200 = 0.02 m/pixel
        
        roi = (10, 20, 100, 50)  # x, y, width, height
        truck_box = (0, 0, 300, 200)  # x1, y1, x2, y2
        truck_height_m = 4.0
        
        width_m, height_m = self.calculator.calculate(roi, truck_box, truck_height_m)
        
        # Expected: width = 100 * 0.02 = 2.0m, height = 50 * 0.02 = 1.0m
        self.assertAlmostEqual(width_m, 2.0, places=2)
        self.assertAlmostEqual(height_m, 1.0, places=2)
    
    def test_calculate_different_scales(self):
        """Test calculation with different scale factors"""
        roi = (0, 0, 50, 25)
        truck_box = (0, 0, 400, 100)  # Height = 100 pixels
        truck_height_m = 3.5
        
        width_m, height_m = self.calculator.calculate(roi, truck_box, truck_height_m)
        
        # Scale: 3.5/100 = 0.035 m/pixel
        # Expected: width = 50 * 0.035 = 1.75m, height = 25 * 0.035 = 0.875m
        self.assertAlmostEqual(width_m, 1.75, places=2)
        self.assertAlmostEqual(height_m, 0.875, places=3)
    
    def test_calculate_scale(self):
        """Test scale factor calculation"""
        scale = self.calculator.calculate_scale(200, 4.0)  # 200 pixels = 4.0 meters
        
        self.assertAlmostEqual(scale, 0.02, places=4)  # 0.02 m/pixel
    
    def test_calculate_scale_edge_cases(self):
        """Test scale calculation with edge cases"""
        # Very small reference
        scale = self.calculator.calculate_scale(10, 0.1)
        self.assertAlmostEqual(scale, 0.01, places=4)
        
        # Very large reference  
        scale = self.calculator.calculate_scale(1000, 10.0)
        self.assertAlmostEqual(scale, 0.01, places=4)
    
    def test_calculate_scale_invalid_input(self):
        """Test scale calculation with invalid inputs"""
        # Zero pixels
        with self.assertRaises(ValueError):
            self.calculator.calculate_scale(0, 1.0)
        
        # Negative pixels
        with self.assertRaises(ValueError):
            self.calculator.calculate_scale(-10, 1.0)
        
        # Zero meters
        with self.assertRaises(ValueError):
            self.calculator.calculate_scale(100, 0)
        
        # Negative meters
        with self.assertRaises(ValueError):
            self.calculator.calculate_scale(100, -1.0)
    
    def test_pixel_to_meters(self):
        """Test pixel to meter conversion"""
        scale = 0.025  # 0.025 m/pixel
        
        result = self.calculator.pixel_to_meters(100, scale)
        self.assertAlmostEqual(result, 2.5, places=2)
        
        result = self.calculator.pixel_to_meters(40, scale)
        self.assertAlmostEqual(result, 1.0, places=2)
    
    def test_meters_to_pixels(self):
        """Test meter to pixel conversion"""
        scale = 0.02  # 0.02 m/pixel
        
        result = self.calculator.meters_to_pixels(1.0, scale)
        self.assertAlmostEqual(result, 50.0, places=1)
        
        result = self.calculator.meters_to_pixels(2.5, scale)
        self.assertAlmostEqual(result, 125.0, places=1)
    
    def test_meters_to_pixels_invalid_scale(self):
        """Test meter to pixel conversion with invalid scale"""
        with self.assertRaises(ValueError):
            self.calculator.meters_to_pixels(1.0, 0)
        
        with self.assertRaises(ValueError):
            self.calculator.meters_to_pixels(1.0, -0.01)
    
    def test_calculate_area(self):
        """Test area calculation"""
        area = self.calculator.calculate_area(2.0, 1.5)
        self.assertAlmostEqual(area, 3.0, places=2)
        
        area = self.calculator.calculate_area(0.5, 0.3)
        self.assertAlmostEqual(area, 0.15, places=3)
    
    def test_validate_measurements_valid(self):
        """Test validation of valid measurements"""
        # Normal measurements
        self.assertTrue(self.calculator.validate_measurements((1.5, 0.8)))
        self.assertTrue(self.calculator.validate_measurements((5.0, 3.0)))
    
    def test_validate_measurements_invalid(self):
        """Test validation of invalid measurements"""
        # Zero measurements
        self.assertFalse(self.calculator.validate_measurements((0, 1.0)))
        self.assertFalse(self.calculator.validate_measurements((1.0, 0)))
        
        # Negative measurements
        self.assertFalse(self.calculator.validate_measurements((-1.0, 1.0)))
        self.assertFalse(self.calculator.validate_measurements((1.0, -0.5)))
        
        # Too large measurements (default max is 10.0m)
        self.assertFalse(self.calculator.validate_measurements((15.0, 5.0)))
        self.assertFalse(self.calculator.validate_measurements((5.0, 12.0)))
    
    def test_validate_measurements_custom_max(self):
        """Test validation with custom maximum size"""
        # Should pass with higher limit
        self.assertTrue(self.calculator.validate_measurements((15.0, 8.0), max_reasonable_size=20.0))
        
        # Should fail with lower limit
        self.assertFalse(self.calculator.validate_measurements((8.0, 6.0), max_reasonable_size=5.0))
    
    def test_precision_and_rounding(self):
        """Test precision handling in calculations"""
        roi = (0, 0, 33, 17)  # Dimensions that create non-round results
        truck_box = (0, 0, 300, 150)  # Height = 150 pixels
        truck_height_m = 3.75
        
        width_m, height_m = self.calculator.calculate(roi, truck_box, truck_height_m)
        
        # Scale: 3.75/150 = 0.025 m/pixel
        # Expected: width = 33 * 0.025 = 0.825m, height = 17 * 0.025 = 0.425m
        self.assertAlmostEqual(width_m, 0.825, places=3)
        self.assertAlmostEqual(height_m, 0.425, places=3)


if __name__ == '__main__':
    unittest.main()