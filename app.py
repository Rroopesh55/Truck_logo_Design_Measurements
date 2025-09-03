#!/usr/bin/env python3
"""
Streamlit Web Interface for Truck Measurement System

A user-friendly web application that allows users to upload truck images
and measure logos/designs through an interactive interface.
"""

import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from PIL import Image
import io
import base64
from pathlib import Path

# Import our truck measurement system
from truck_measurement import (
    TruckDetector,
    TruckClassifier, 
    MeasurementCalculator,
    ImageVisualizer
)
from truck_measurement.utils import setup_logging

# Configure page
st.set_page_config(
    page_title="Truck Measurement System",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2e86ab;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitTruckMeasurement:
    """
    Streamlit interface for the truck measurement system
    """
    
    def __init__(self):
        """Initialize the measurement system components"""
        if 'detector' not in st.session_state:
            with st.spinner("Loading AI models... This may take a moment on first run."):
                try:
                    st.session_state.detector = TruckDetector()
                    st.session_state.classifier = TruckClassifier()
                    st.session_state.calculator = MeasurementCalculator()
                    st.session_state.visualizer = ImageVisualizer()
                    st.session_state.models_loaded = True
                except Exception as e:
                    st.session_state.models_loaded = False
                    st.session_state.model_error = str(e)
    
    def save_uploaded_file(self, uploaded_file):
        """
        Save uploaded file to temporary location
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            str: Path to saved file
        """
        try:
            # Create temporary file
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                return tmp_file.name
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return None
    
    def load_image(self, image_path):
        """
        Load image from path
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            numpy.ndarray: Loaded image
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                st.error("Could not load image. Please check the file format.")
                return None
            return image
        except Exception as e:
            st.error(f"Error loading image: {e}")
            return None
    
    def detect_truck(self, image):
        """
        Detect truck in image
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            tuple: (truck_box, confidence) or (None, None)
        """
        try:
            detections = st.session_state.detector.detect_trucks(image)
            if not detections:
                return None, None
            
            best_detection = st.session_state.detector.get_best_detection(detections)
            truck_box = best_detection[:4]
            confidence = best_detection[4]
            
            return truck_box, confidence
        except Exception as e:
            st.error(f"Error detecting truck: {e}")
            return None, None
    
    def classify_truck(self, truck_box):
        """
        Classify truck type
        
        Args:
            truck_box (tuple): Truck bounding box
            
        Returns:
            tuple: (truck_type, truck_height)
        """
        try:
            x1, y1, x2, y2 = truck_box
            bbox_width = x2 - x1
            bbox_height = y2 - y1
            
            return st.session_state.classifier.classify(bbox_width, bbox_height)
        except Exception as e:
            st.error(f"Error classifying truck: {e}")
            return "Unknown", 3.5
    
    def create_clickable_image(self, image, truck_box=None, truck_type=None, truck_height=None):
        """
        Create an image with truck detection overlay
        
        Args:
            image (numpy.ndarray): Input image
            truck_box (tuple): Truck bounding box
            truck_type (str): Truck type
            truck_height (float): Truck height
            
        Returns:
            numpy.ndarray: Processed image
        """
        display_image = image.copy()
        
        if truck_box is not None:
            st.session_state.visualizer.draw_truck_detection(
                display_image, truck_box, truck_type, truck_height
            )
        
        return display_image
    
    def calculate_measurements(self, roi, truck_box, truck_height):
        """
        Calculate measurements for selected ROI
        
        Args:
            roi (tuple): Region of interest
            truck_box (tuple): Truck bounding box
            truck_height (float): Truck height
            
        Returns:
            tuple: (width_m, height_m) or None
        """
        try:
            return st.session_state.calculator.calculate(roi, truck_box, truck_height)
        except Exception as e:
            st.error(f"Error calculating measurements: {e}")
            return None
    
    def create_result_image(self, image, truck_box, truck_type, truck_height, roi, measurements):
        """
        Create final result image with all annotations
        
        Args:
            image (numpy.ndarray): Original image
            truck_box (tuple): Truck bounding box
            truck_type (str): Truck type
            truck_height (float): Truck height
            roi (tuple): Selected region
            measurements (tuple): Calculated measurements
            
        Returns:
            numpy.ndarray: Final annotated image
        """
        result_image = image.copy()
        
        # Draw truck detection
        st.session_state.visualizer.draw_truck_detection(
            result_image, truck_box, truck_type, truck_height
        )
        
        # Draw measurements
        st.session_state.visualizer.draw_measurements(
            result_image, roi, measurements
        )
        
        # Add scale bar
        truck_pixel_height = truck_box[3] - truck_box[1]
        pixels_per_meter = truck_pixel_height / truck_height
        st.session_state.visualizer.draw_scale_bar(
            result_image, 1.0, pixels_per_meter, (50, 50)
        )
        
        return result_image
    
    def cv2_to_pil(self, cv2_image):
        """Convert OpenCV image to PIL Image"""
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)
    
    def pil_to_bytes(self, pil_image):
        """Convert PIL Image to bytes for download"""
        img_bytes = io.BytesIO()
        pil_image.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
    
    def run(self):
        """Run the Streamlit application"""
        # Header
        st.markdown('<h1 class="main-header">🚛 Truck Logo Measurement System</h1>', 
                   unsafe_allow_html=True)
        
        # Check if models are loaded
        if not st.session_state.get('models_loaded', False):
            st.error("❌ Failed to load AI models!")
            if 'model_error' in st.session_state:
                st.error(f"Error: {st.session_state.model_error}")
            st.markdown("""
            **Possible solutions:**
            1. Check your internet connection (needed to download YOLO model)
            2. Restart the application
            3. Check the logs for detailed error information
            """)
            return
        
        # Sidebar for controls
        with st.sidebar:
            st.markdown('<h2 class="sub-header">⚙️ Controls</h2>', unsafe_allow_html=True)
            
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose a truck image",
                type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
                help="Upload a clear image of a truck taken from the side"
            )
            
            # Settings
            st.markdown("### Settings")
            resize_scale = st.slider(
                "Display Scale",
                min_value=0.1,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Adjust image size for display and processing"
            )
            
            show_grid = st.checkbox("Show Grid Overlay", value=False)
            show_scale_bar = st.checkbox("Show Scale Bar", value=True)
            
            # Instructions
            st.markdown("""
            ### 📋 Instructions
            1. **Upload** a truck image
            2. **Wait** for automatic detection
            3. **Click** on the logo/design area to measure
            4. **View** results and download
            
            ### 💡 Tips
            - Use clear, side-view truck photos
            - Ensure good lighting
            - Take photos perpendicular to truck
            - Higher resolution = better accuracy
            """)
        
        # Main content area
        if uploaded_file is not None:
            # Save uploaded file
            temp_path = self.save_uploaded_file(uploaded_file)
            if temp_path is None:
                return
            
            # Load and process image
            image = self.load_image(temp_path)
            if image is None:
                return
            
            # Resize image
            original_image = image.copy()
            if resize_scale != 1.0:
                image = cv2.resize(image, (0, 0), fx=resize_scale, fy=resize_scale)
            
            # Create columns for layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<h2 class="sub-header">📸 Image Analysis</h2>', 
                           unsafe_allow_html=True)
                
                # Detect truck
                with st.spinner("🔍 Detecting truck..."):
                    truck_box, confidence = self.detect_truck(image)
                
                if truck_box is None:
                    st.error("❌ No truck detected in the image!")
                    st.markdown("""
                    **Suggestions:**
                    - Try a different image with a clearer truck view
                    - Adjust the display scale
                    - Ensure the truck is the main subject in the image
                    """)
                    # Still show the image
                    st.image(self.cv2_to_pil(image), caption="Uploaded Image", use_column_width=True)
                else:
                    # Classify truck
                    truck_type, truck_height = self.classify_truck(truck_box)
                    
                    # Create image with detection overlay
                    display_image = self.create_clickable_image(
                        image, truck_box, truck_type, truck_height
                    )
                    
                    # Add grid if requested
                    if show_grid:
                        st.session_state.visualizer.draw_grid(display_image, spacing=50)
                    
                    # Display image
                    st.image(
                        self.cv2_to_pil(display_image), 
                        caption=f"Detected: {truck_type} (Confidence: {confidence:.2f})",
                        use_column_width=True
                    )
                    
                    # ROI Selection Interface
                    st.markdown("### 🎯 Select Measurement Area")
                    st.info("Use the sliders below to select the logo/design area for measurement")
                    
                    # Get image dimensions
                    img_height, img_width = display_image.shape[:2]
                    
                    # ROI selection sliders
                    col_x, col_y = st.columns(2)
                    with col_x:
                        roi_x = st.slider("X Position", 0, img_width-50, 50)
                        roi_width = st.slider("Width", 10, img_width-roi_x, 100)
                    
                    with col_y:
                        roi_y = st.slider("Y Position", 0, img_height-50, 100)
                        roi_height = st.slider("Height", 10, img_height-roi_y, 50)
                    
                    roi = (roi_x, roi_y, roi_width, roi_height)
                    
                    # Calculate measurements
                    measurements = self.calculate_measurements(roi, truck_box, truck_height)
                    
                    if measurements:
                        width_m, height_m = measurements
                        area_m2 = width_m * height_m
                        
                        # Create final result image
                        result_image = self.create_result_image(
                            display_image.copy(), truck_box, truck_type, truck_height, roi, measurements
                        )
                        
                        # Show result
                        st.markdown("### 📏 Measurement Result")
                        st.image(
                            self.cv2_to_pil(result_image),
                            caption="Final Measurement Result",
                            use_column_width=True
                        )
            
            with col2:
                st.markdown('<h2 class="sub-header">📊 Results</h2>', unsafe_allow_html=True)
                
                if truck_box is not None:
                    # Detection results
                    st.markdown("""
                    <div class="metric-container">
                        <h3>🚛 Truck Detection</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Truck Type", truck_type)
                    st.metric("Standard Height", f"{truck_height:.2f} m")
                    st.metric("Detection Confidence", f"{confidence:.2%}")
                    
                    # Measurement results
                    if 'measurements' in locals() and measurements:
                        st.markdown("""
                        <div class="metric-container">
                            <h3>📏 Measurements</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.metric("Width", f"{width_m:.3f} m", f"{width_m*100:.1f} cm")
                        st.metric("Height", f"{height_m:.3f} m", f"{height_m*100:.1f} cm")
                        st.metric("Area", f"{area_m2:.4f} m²", f"{area_m2*10000:.2f} cm²")
                        
                        # Validation
                        is_valid = st.session_state.calculator.validate_measurements(measurements)
                        if is_valid:
                            st.success("✅ Measurements appear reasonable")
                        else:
                            st.warning("⚠️ Measurements may be inaccurate - please verify")
                        
                        # Download button
                        if 'result_image' in locals():
                            result_bytes = self.pil_to_bytes(self.cv2_to_pil(result_image))
                            st.download_button(
                                label="📥 Download Result",
                                data=result_bytes,
                                file_name=f"truck_measurement_{truck_type.replace(' ', '_').lower()}.png",
                                mime="image/png"
                            )
                        
                        # Additional info
                        st.markdown("""
                        <div class="info-box">
                            <h4>📈 Accuracy Info</h4>
                            <p>Typical accuracy: ±10-15cm under normal conditions</p>
                            <p>Best accuracy achieved with perpendicular side-view photos</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Technical details expander
                with st.expander("🔧 Technical Details"):
                    if truck_box is not None:
                        x1, y1, x2, y2 = truck_box
                        st.write(f"**Truck Box:** ({x1}, {y1}) to ({x2}, {y2})")
                        st.write(f"**Box Dimensions:** {x2-x1} × {y2-y1} pixels")
                        st.write(f"**Scale Factor:** {truck_height/(y2-y1):.6f} m/pixel")
                        
                        if 'roi' in locals():
                            st.write(f"**ROI:** {roi}")
                            st.write(f"**ROI Pixels:** {roi[2]} × {roi[3]}")
                    
                    st.write(f"**Image Dimensions:** {image.shape[1]} × {image.shape[0]}")
                    st.write(f"**Display Scale:** {resize_scale}")
        else:
            # Landing page when no image is uploaded
            st.markdown("""
            <div class="info-box">
                <h2>🚀 Welcome to the Truck Measurement System!</h2>
                <p>This AI-powered tool helps you measure logos and designs on truck surfaces with high accuracy.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                ### 🎯 How it Works
                1. **Upload** a truck image
                2. **AI detects** and classifies the truck
                3. **Select** the area to measure
                4. **Get** precise measurements in meters
                """)
            
            with col2:
                st.markdown("""
                ### 📊 Features
                - **Automatic truck detection**
                - **5 truck types supported**
                - **Real-world measurements**
                - **High accuracy (±10-15cm)**
                - **Download results**
                """)
            
            with col3:
                st.markdown("""
                ### 💡 Best Practices
                - Use **side-view** photos
                - Ensure **good lighting**
                - Take photos **perpendicular** to truck
                - Use **high resolution** images
                """)
            
            # Sample images showcase
            st.markdown("### 📸 Sample Results")
            st.info("Upload your truck image using the sidebar to get started!")
        
        # Cleanup temporary file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        
        # Footer
        st.markdown("""
        ---
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
            🚛 Truck Measurement System v1.0 | Built with Streamlit & YOLOv5
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main entry point for the Streamlit app"""
    # Setup logging
    setup_logging("INFO")
    
    # Initialize and run the app
    app = StreamlitTruckMeasurement()
    app.run()


if __name__ == "__main__":
    main()