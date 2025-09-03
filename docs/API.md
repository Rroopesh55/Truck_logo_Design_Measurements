# API Documentation

## Overview

The Truck Measurement System provides a comprehensive API for programmatic access to truck detection, classification, and measurement capabilities.

## Core Classes

### TruckMeasurementSystem

Main system class that orchestrates the complete measurement process.

```python
from truck_measurement import TruckMeasurementSystem

system = TruckMeasurementSystem(resize_scale=0.6)
```

#### Methods

##### `__init__(resize_scale=0.6)`
Initialize the measurement system.

**Parameters:**
- `resize_scale` (float): Scale factor for image display (0.1-1.0)

##### `process_image(image_path, output_path=None)`
Process a truck image and perform measurements.

**Parameters:**
- `image_path` (str): Path to input image
- `output_path` (str, optional): Path to save result image

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
system = TruckMeasurementSystem()
success = system.process_image("truck.jpg", "result.jpg")
```

---

### TruckDetector

YOLO-based truck detection class.

```python
from truck_measurement import TruckDetector

detector = TruckDetector()
```

#### Methods

##### `__init__(model_path=None)`
Initialize the truck detector.

**Parameters:**
- `model_path` (str, optional): Path to YOLO model file

##### `detect_trucks(image)`
Detect trucks in the given image.

**Parameters:**
- `image` (numpy.ndarray): Input image

**Returns:**
- `list`: List of truck detections [(x1, y1, x2, y2, confidence), ...]

**Example:**
```python
import cv2
detector = TruckDetector()
image = cv2.imread("truck.jpg")
detections = detector.detect_trucks(image)
```

##### `get_best_detection(detections)`
Get the truck detection with highest confidence.

**Parameters:**
- `detections` (list): List of truck detections

**Returns:**
- `tuple`: Best detection (x1, y1, x2, y2, confidence) or None

##### `is_model_loaded()`
Check if YOLO model is loaded.

**Returns:**
- `bool`: True if model is loaded, False otherwise

---

### TruckClassifier

Classifies truck types based on bounding box dimensions.

```python
from truck_measurement import TruckClassifier

classifier = TruckClassifier()
```

#### Methods

##### `classify(bbox_width, bbox_height)`
Classify truck type based on bounding box dimensions.

**Parameters:**
- `bbox_width` (int): Bounding box width in pixels
- `bbox_height` (int): Bounding box height in pixels

**Returns:**
- `tuple`: (truck_type, truck_height_meters)

**Example:**
```python
classifier = TruckClassifier()
truck_type, height = classifier.classify(300, 200)
print(f"Type: {truck_type}, Height: {height}m")
```

##### `get_truck_height(truck_type)`
Get the standard height for a truck type.

**Parameters:**
- `truck_type` (str): Type of truck

**Returns:**
- `float`: Height in meters

##### `get_all_truck_types()`
Get all supported truck types.

**Returns:**
- `dict`: Dictionary of truck types and their heights

##### `validate_classification(truck_type)`
Validate if truck type is supported.

**Parameters:**
- `truck_type` (str): Truck type to validate

**Returns:**
- `bool`: True if valid, False otherwise

---

### MeasurementCalculator

Calculates real-world measurements from pixel dimensions.

```python
from truck_measurement import MeasurementCalculator

calculator = MeasurementCalculator()
```

#### Methods

##### `calculate(roi, truck_box, truck_height_m)`
Calculate real-world measurements of the selected region.

**Parameters:**
- `roi` (tuple): Selected region (x, y, width, height)
- `truck_box` (tuple): Truck bounding box (x1, y1, x2, y2)
- `truck_height_m` (float): Truck height in meters

**Returns:**
- `tuple`: (width_meters, height_meters)

**Example:**
```python
calculator = MeasurementCalculator()
roi = (10, 20, 100, 50)
truck_box = (0, 0, 300, 200)
truck_height = 4.0

width_m, height_m = calculator.calculate(roi, truck_box, truck_height)
```

##### `calculate_scale(reference_pixels, reference_meters)`
Calculate pixels per meter scale factor.

**Parameters:**
- `reference_pixels` (float): Reference length in pixels
- `reference_meters` (float): Reference length in meters

**Returns:**
- `float`: Scale factor (meters per pixel)

##### `pixel_to_meters(pixel_value, scale)`
Convert pixel measurement to meters.