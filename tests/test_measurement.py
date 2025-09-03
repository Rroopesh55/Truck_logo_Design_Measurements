import unittest
from truck_measurement import MeasurementCalculator  # via __init__.py

class TestMeasurementCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = MeasurementCalculator()

    def test_calculate_scale_and_conversion(self):
        scale = self.calc.calculate_scale(200, 4.0)
        self.assertAlmostEqual(scale, 0.02)

        meters = self.calc.pixel_to_meters(100, scale)
        self.assertAlmostEqual(meters, 2.0)

        pixels = self.calc.meters_to_pixels(2.0, scale)
        self.assertAlmostEqual(pixels, 100.0)

    def test_measurement_calculation(self):
        roi = (10, 20, 100, 50)
        truck_box = (0, 0, 300, 200)
        height_m = 4.0
        width_m, height_m2 = self.calc.calculate(roi, truck_box, height_m)
        self.assertAlmostEqual(width_m, 2.0)
        self.assertAlmostEqual(height_m2, 1.0)

    def test_area_and_validation(self):
        area = self.calc.calculate_area(2.0, 1.5)
        self.assertAlmostEqual(area, 3.0)

        self.assertTrue(self.calc.validate_measurements((1.0, 2.0)))
        self.assertFalse(self.calc.validate_measurements((-1.0, 2.0)))
        self.assertFalse(self.calc.validate_measurements((5.0, 12.0)))
