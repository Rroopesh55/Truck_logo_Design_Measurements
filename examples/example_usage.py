#!/usr/bin/env python3
"""
Example usage of the Truck Measurement System

This script demonstrates how to use the various components
of the truck measurement system programmatically.
"""

import cv2
import numpy as np
import logging
from pathlib import Path

# Import the truck measurement system components
from truck_measurement import (
    TruckMeasurementSystem,
    TruckDetector,
    TruckClassifier,
    MeasurementCalculator,
    ImageVisualizer
)
from truck_measurement.utils import setup_logging


def create_sample_image():
    """
    Create a sample image with a truck-like rectangle for demonstration
    
    Returns:
        numpy.ndarray: Sample image
    """
    # Create a blank image
    image = np.ones((400, 600, 3), dtype=np.uint8) * 200  # Light gray background
    
    # Draw a truck-like rectangle
    cv2.rectangle(image, (50, 150), (350, 250), (100, 100, 100), -1)  # Truck body
    cv2.rectangle(image, (350, 170), (400, 230), (80, 80, 80), -1)    # Truck cab
    
    # Add some text
    cv2.putText(image, "SAMPLE TRUCK", (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (255, 255, 255), 2)
    
    return image


def example_complete_measurement():
    """
    Example of complete measurement process using the main system class
    """
    print("=" * 60)
    print("EXAMPLE 1: Complete Measurement Process")
    print("=" * 60)
    
    # Setup logging
    setup_logging("INFO")
    
    # Initialize the system
    system = TruckMeasurementSystem(resize_scale=0.6)
    
    # Example image path (replace with your actual image)
    image_path = "examples/sample_truck.jpg"
    output_path = "examples/result.jpg"
    
    if Path(image_path).exists():
        # Process the image
        success = system.process_image(image_path, output_path)
        
        if success:
            print("✓ Measurement completed successfully!")
        else:
            print("✗ Measurement failed!")
    else:
        print(f"⚠ Sample image not found at {image_path}")
        print("Please add a truck image to test the system.")


def example_individual_components():
    """
    Example of using individual components separately
    """
    print("=" * 60)
    print("EXAMPLE 2: Individual Components Usage")
    print("=" * 60)
    
    # Create a sample image for demonstration
    sample_image = create_sample_image()
    
    # 1. Initialize components
    detector = TruckDetector()
    classifier = TruckClassifier()
    calculator = MeasurementCalculator()
    visualizer = ImageVisualizer()
    
    print("✓ Components initialized")
    
    # 2. Detect trucks (simulated)
    print("- Simulating truck detection...")
    simulated_detection = (50, 150, 350, 250, 0.95)  # x1, y1, x2, y2, confidence
    truck_box = simulated_detection[:4]
    
    # 3. Classify truck
    bbox_width = truck_box[2] - truck_box[0]
    bbox_height = truck_box[3] - truck_box[1]
    truck_type, truck_height = classifier.classify(bbox_width, bbox_height)
    
    print(f"- Classified as: {truck_type} ({truck_height}m)")
    
    # 4. Simulate ROI selection
    roi = (120, 180, 80, 40)  # x, y, width, height (logo area)
    
    # 5. Calculate measurements
    measurements = calculator.calculate(roi, truck_box, truck_height)
    width_m, height_m = measurements
    
    print(f"- Calculated measurements: {width_m:.2f}m x {height_m:.2f}m")
    
    # 6. Visualize results
    visualizer.draw_truck_detection(sample_image, truck_box, truck_type, truck_height)
    visualizer.draw_measurements(sample_image, roi, measurements)
    
    # Add scale bar for reference
    scale = truck_height / bbox_height
    pixels_per_meter = 1 / scale
    visualizer.draw_scale_bar(sample_image, 1.0, pixels_per_meter, (450, 350))
    
    # Display the result
    cv2.imshow("Example Result", sample_image)
    print("- Press any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("✓ Individual components example completed!")


def example_custom_truck_classification():
    """
    Example of using the truck classifier with different inputs
    """
    print("=" * 60)
    print("EXAMPLE 3: Custom Truck Classification")
    print("=" * 60)
    
    classifier = TruckClassifier()
    
    # Test different bounding box dimensions
    test_cases = [
        (400, 250, "Large truck with high aspect ratio"),
        (300, 200, "Large truck with moderate aspect ratio"),
        (200, 160, "Medium sized truck"),
        (150, 130, "Small-medium truck"),
        (100, 100, "Small truck")
    ]
    
    for width, height, description in test_cases:
        truck_type, truck_height = classifier.classify(width, height)
        aspect_ratio = width / height
        
        print(f"- {description}")
        print(f"  Dimensions: {width}x{height} px (AR: {aspect_ratio:.2f})")
        print(f"  Classification: {truck_type} ({truck_height}m)")
        print()
    
    # Show all supported truck types
    print("All supported truck types:")
    for truck_type, height in classifier.get_all_truck_types().items():
        print(f"- {truck_type}: {height}m")


def example_measurement_calculations():
    """
    Example of various measurement calculations
    """
    print("=" * 60)
    print("EXAMPLE 4: Measurement Calculations")
    print("=" * 60)
    
    calculator = MeasurementCalculator()
    
    # Example 1: Basic calculation
    print("Example 1: Basic measurement calculation")
    roi = (10, 20, 100, 50)  # x, y, width, height
    truck_box = (0, 0, 300, 200)  # x1, y1, x2, y2  
    truck_height_m = 4.0
    
    width_m, height_m = calculator.calculate(roi, truck_box, truck_height_m)
    print(f"ROI: {roi[2]}x{roi[3]} pixels")
    print(f"Truck height: {truck_box[3] - truck_box[1]} pixels = {truck_height_m}m")
    print(f"Scale: {truck_height_m / (truck_box[3] - truck_box[1]):.4f} m/pixel")
    print(f"Measurements: {width_m:.2f}m x {height_m:.2f}m")
    print(f"Area: {calculator.calculate_area(width_m, height_m):.2f} m²")
    print()
    
    # Example 2: Different scale factors
    print("Example 2: Different scale factors")
    scales_and_trucks = [
        (0.01, "Large detailed image"),
        (0.02, "Medium resolution image"), 
        (0.05, "Small or distant image")
    ]
    
    pixel_measurement = 80  # pixels
    
    for scale, description in scales_and_trucks:
        real_measurement = calculator.pixel_to_meters(pixel_measurement, scale)
        print(f"- {description}: {scale:.3f} m/pixel")
        print(f"  {pixel_measurement} pixels = {real_measurement:.2f} meters")
        print()
    
    # Example 3: Validation
    print("Example 3: Measurement validation")
    test_measurements = [
        (1.5, 0.8, "Normal logo"),
        (0.2, 0.1, "Small decal"),
        (5.0, 3.0, "Large side panel"),
        (15.0, 8.0, "Unreasonably large"),
        (-1.0, 2.0, "Invalid negative")
    ]
    
    for width, height, description in test_measurements:
        is_valid = calculator.validate_measurements((width, height))
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"- {description}: {width}m x {height}m - {status}")


def example_visualization_features():
    """
    Example of various visualization features
    """
    print("=" * 60)
    print("EXAMPLE 5: Visualization Features")
    print("=" * 60)
    
    visualizer = ImageVisualizer()
    
    # Create sample image
    image = create_sample_image()
    
    # Example truck detection
    truck_box = (50, 150, 350, 250)
    truck_type = "Box Truck"
    truck_height = 3.96
    
    # Example ROI and measurements
    roi = (120, 180, 80, 40)
    measurements = (1.2, 0.6)  # meters
    
    print("- Drawing truck detection...")
    visualizer.draw_truck_detection(image, truck_box, truck_type, truck_height)
    
    print("- Drawing measurements...")
    visualizer.draw_measurements(image, roi, measurements)
    
    print("- Adding scale bar...")
    pixels_per_meter = 100  # example scale
    visualizer.draw_scale_bar(image, 1.0, pixels_per_meter, (450, 320))
    
    print("- Adding crosshair at logo center...")
    roi_center = (roi[0] + roi[2]//2, roi[1] + roi[3]//2)
    visualizer.draw_crosshair(image, roi_center, size=15)
    
    print("- Adding grid overlay...")
    grid_image = image.copy()
    visualizer.draw_grid(grid_image, spacing=50)
    
    # Create info panel
    print("- Creating info panel...")
    info_panel = visualizer.create_info_panel(300, 200)
    info_data = {
        "Truck Type": truck_type,
        "Height": f"{truck_height}m",
        "Logo Width": f"{measurements[0]:.2f}m",
        "Logo Height": f"{measurements[1]:.2f}m",
        "Area": f"{measurements[0] * measurements[1]:.2f}m²"
    }
    visualizer.add_info_to_panel(info_panel, info_data)
    
    # Combine images
    combined = visualizer.combine_images_horizontal(image, info_panel)
    
    # Display results
    cv2.imshow("Visualization Features", image)
    cv2.imshow("With Grid", grid_image)
    cv2.imshow("Combined with Info Panel", combined)
    
    print("- Press any key to close all windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("✓ Visualization examples completed!")


def main():
    """
    Run all examples
    """
    print("🚛 TRUCK MEASUREMENT SYSTEM - EXAMPLES")
    print("=" * 60)
    
    try:
        # Run examples
        example_complete_measurement()
        print("\n")
        
        example_individual_components()
        print("\n")
        
        example_custom_truck_classification()
        print("\n")
        
        example_measurement_calculations()
        print("\n")
        
        example_visualization_features()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()