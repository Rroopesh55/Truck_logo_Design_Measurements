import unittest
from truck_measurement import TruckClassifier  # via __init__.py

class TestTruckClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = TruckClassifier()

    def test_classify_semi_trailer(self):
        ttype, height = self.classifier.classify(500, 180)
        self.assertEqual(ttype, "Semi Trailer")
        self.assertEqual(height, 4.0)

    def test_classify_box_truck(self):
        ttype, height = self.classifier.classify(300, 220)
        self.assertEqual(ttype, "Box Truck")
        self.assertEqual(height, 3.5)

    def test_classify_cube_van(self):
        ttype, height = self.classifier.classify(200, 170)
        self.assertEqual(ttype, "Cube Van")
        self.assertEqual(height, 3.0)

    def test_classify_sprinter_van(self):
        ttype, height = self.classifier.classify(180, 130)
        self.assertEqual(ttype, "Sprinter Van")
        self.assertEqual(height, 2.5)

    def test_classify_cargo_van(self):
        ttype, height = self.classifier.classify(150, 100)
        self.assertEqual(ttype, "Cargo Van")
        self.assertEqual(height, 2.0)

    def test_edge_cases(self):
        ttype, _ = self.classifier.classify(1000, 300)
        self.assertEqual(ttype, "Semi Trailer")

        ttype, _ = self.classifier.classify(50, 30)
        self.assertEqual(ttype, "Cargo Van")

        # borderline (change as needed for your thresholds/logic)
        ttype, _ = self.classifier.classify(200, 200)
        self.assertIn(ttype, {"Box Truck", "Cube Van"})  # allow either based on AR/threshold
