# Usage Guide

This guide provides detailed instructions for using the Truck Measurement System.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Command Line Usage](#command-line-usage)
3. [Programmatic Usage](#programmatic-usage)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Features](#advanced-features)

## Quick Start

### 1. Installation

```bash
# Clone and install
git clone https://github.com/yourusername/truck-measurement-system.git
cd truck-measurement-system
pip install -e .
```

### 2. Basic Usage

```bash
# Measure objects on a truck image
python -m truck_measurement your_truck_image.jpg
```

### 3. Interactive Workflow

1. **Image loads** - The system displays your truck image
2. **Automatic detection** - Green box appears around detected truck
3. **Select region** - Click and drag to select logo/design area
4. **View results** - Measurements appear on image and in console

## Command Line Usage

### Basic Commands

```bash
# Basic measurement
python -m truck_measurement truck.jpg

# Save result image
python -m truck_measurement truck.jpg --output result.jpg

# Enable debug logging
python -m truck_measurement truck.jpg --log-level DEBUG

# Save logs to file
python -m truck_measurement truck.jpg --log-file measurement.log

# Adjust display scale
python -m truck_measurement truck.jpg --resize-scale 0.4
```

### Command Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--output, -o` | Save result image | None | `--output result.jpg` |
| `--log-level` | Logging level | INFO | `--log-level DEBUG` |
| `--log-file` | Log file path | None | `--log-file app.log` |
| `--resize-scale` | Display scale | 0.6 | `--resize-scale 0.8` |
| `--help` | Show help | - | `--help` |
| `--version` | Show version | - | `--version` |

### Examples

```bash
# High precision measurement with detailed logging
python -m truck_measurement truck.jpg \
    --output detailed_result.jpg \
    --log-level DEBUG \
    --log-file measurement.log \
    --resize-scale 0.8

# Quick measurement for small images
python -m truck_measurement small_truck.jpg --resize-scale 1.0

# Batch processing with logging
for image in *.jpg; do
    python -m truck_measurement "$image" \
        --output "result_$image" \
        --log-file batch.log
done
```

## Programmatic Usage

### Simple Measurement

```python
from truck_measurement import TruckMeasurementSystem

# Initialize system
system = TruckMeasurementSystem()

# Process image
success = system.process_image("truck.jpg", "result.jpg")

if success:
    print("✓ Measurement completed!")
else:
    print("✗ Measurement failed!")
```

### Individual Components

```python
import cv2
from truck_measurement import TruckDetector, TruckClassifier, MeasurementCalculator

# Load image
image = cv2.imread("truck.jpg")

# Detect truck
detector = TruckDetector()
detections = detector.detect_trucks(image)

if detections:
    # Get best detection
    best_detection = detector.get_best_detection(detections)
    truck_box = best_detection[:4]
    
    # Classify truck
    classifier = TruckClassifier()
    bbox_width = truck_box[2] - truck_box[0]
    bbox_height = truck_box[3] - truck_box[1]
    truck_type, truck_height = classifier.classify(bbox_width, bbox_height)
    
    print(f"Detected: {truck_type} ({truck_height}m)")
    
    # Calculate measurements (ROI would be from user selection)
    roi = (100, 50, 80, 40)  # x, y, width, height
    calculator = MeasurementCalculator()
    width_m, height_m = calculator.calculate(roi, truck_box, truck_height)
    
    print(f"Measurements: {width_m:.2f}m x {height_m:.2f}m")
```

### Custom Visualization

```python
import cv2
from truck_measurement import ImageVisualizer

visualizer = ImageVisualizer()
image = cv2.imread("truck.jpg")

# Draw truck detection
truck_box = (50, 100, 350, 250)
visualizer.draw_truck_detection(image, truck_box, "Box Truck", 3.96)

# Draw measurements
roi = (150, 150, 100, 50)
measurements = (1.5, 0.75)
visualizer.draw_measurements(image, roi, measurements)

# Add scale bar
visualizer.draw_scale_bar(image, 1.0, 100, (400, 300))

# Display
cv2.imshow("Custom Visualization", image)
cv2.waitKey(0)
```

## Best Practices

### Image Quality

**✅ Good Images:**
- Clear truck visibility
- Good lighting conditions  
- Perpendicular viewing angle
- Minimal obstructions
- High resolution (>1000px width)

**❌ Avoid:**
- Blurry or low-resolution images
- Extreme angles (>30° from perpendicular)
- Heavy shadows or backlighting
- Partially obscured trucks
- Multiple overlapping vehicles

### Measurement Accuracy

**For Best Results:**
1. **Take photos perpendicular to truck side**
2. **Ensure good lighting** - avoid shadows on measurement area
3. **Include full truck height** - needed for scale reference
4. **Use highest camera resolution** available
5. **Keep camera steady** - use tripod if possible

**Typical Accuracy:**
- Perpendicular view, good lighting: ±5-10cm
- Slight angle, normal conditions: ±10-15cm  
- Challenging conditions: ±15-25cm

### ROI Selection Tips

**When selecting logo/design region:**
- **Be precise** - accuracy depends on selection quality
- **Select just the object** - avoid surrounding areas
- **Include clear edges** - helps with visual verification
- **Consistent selection** - for comparing multiple measurements

## Troubleshooting

### Common Issues

#### "No truck detected"

**Causes:**
- Truck not clearly visible
- Poor image quality
- Unusual truck type

**Solutions:**
```bash
# Try different resize scale
python -m truck_measurement truck.jpg --resize-scale 0.8

# Enable debug logging to see detection details
python -m truck_measurement truck.jpg --log-level DEBUG
```

#### "Model download failed"

**Causes:**
- No internet connection
- Firewall blocking downloads
- Insufficient disk space

**Solutions:**
```bash
# Manual model download
curl -L https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt -o yolov5s.pt

# Check available space
df -h
```

#### "Inaccurate measurements"

**Causes:**
- Angled photography
- Wrong truck classification
- Poor ROI selection

**Solutions:**
1. Retake photo from perpendicular angle
2. Verify truck type in output
3. Re-select region more precisely

#### "Import errors"

**Common fix:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Install in development mode
pip install -e .
```

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
python -m truck_measurement truck.jpg \
    --log-level DEBUG \
    --log-file debug.log

# Then check the log file
cat debug.log
```

### Performance Issues

**Large Images:**
```bash
# Reduce processing size
python -m truck_measurement large_truck.jpg --resize-scale 0.4
```

**Slow Detection:**
- Ensure you have adequate RAM (4GB+ recommended)
- Consider GPU acceleration (CUDA-capable card)
- Close other applications during processing

## Advanced Features

### Batch Processing

```python
import os
from truck_measurement import TruckMeasurementSystem

system = TruckMeasurementSystem()

# Process all images in directory
image_dir = "truck_images"
output_dir = "results"

for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(image_dir, filename)
        output_path = os.path.join(output_dir, f"measured_{filename}")
        
        success = system.process_image(input_path, output_path)
        print(f"{filename}: {'✓' if success else '✗'}")
```

### Custom Configuration

```python
# Modify truck heights for custom vehicles
from truck_measurement.config import TRUCK_HEIGHTS

TRUCK_HEIGHTS["Custom Truck"] = 4.5  # meters

# Adjust classification thresholds
from truck_measurement.config import HEIGHT_THRESHOLDS

HEIGHT_THRESHOLDS["large"] = 250  # pixels
```

### Integration with Other Tools

```python
# Save measurements to CSV
import csv
from truck_measurement import TruckMeasurementSystem

system = TruckMeasurementSystem()

# Your measurement logic here...
# measurements = [(filename, width, height, area), ...]

with open('measurements.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Filename', 'Width_m', 'Height_m', 'Area_m2'])
    writer.writerows(measurements)
```

### API Integration

```python
from flask import Flask, request, jsonify
from truck_measurement import TruckMeasurementSystem

app = Flask(__name__)
system = TruckMeasurementSystem()

@app.route('/measure', methods=['POST'])
def measure_truck():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Save uploaded file
    image_file = request.files['image']
    temp_path = f"temp_{image_file.filename}"
    image_file.save(temp_path)
    
    # Process
    success = system.process_image(temp_path)
    
    # Return results
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)
```

## Support

- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: See `docs/API.md` for detailed API reference  
- **Examples**: Check `examples/example_usage.py` for code samples

## Next Steps

1. **Try the examples** in `examples/example_usage.py`
2. **Read the API documentation** in `docs/API.md`
3. **Experiment with different truck types** and images
4. **Customize settings** in `truck_measurement/config.py`
5. **Contribute** improvements back to the project!