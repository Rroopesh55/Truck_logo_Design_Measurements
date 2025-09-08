# --- app.py ---
import os, sys
from pathlib import Path

# Ensure project root is on sys.path (so local package is importable)
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import cv2

# Import from your package (works now that folder is truck_measurement/)
from truck_measurement.detector import TruckDetector
from truck_measurement.classifier import TruckClassifier
from truck_measurement.measurement import MeasurementCalculator
from truck_measurement.visualizer import ImageVisualizer

# ---- Streamlit page setup ----
st.set_page_config(page_title="Truck Measurement App", layout="centered")
st.title("🚛 Truck Measurement App")
st.write("Upload a truck image to detect the truck and estimate real-world measurements.")

uploaded_file = st.file_uploader("Upload a truck image", type=["jpg", "jpeg", "png"])
logo_template_file = st.file_uploader("Upload a logo template (for automatic detection)", type=["jpg", "jpeg", "png"], key="logo_template")

# ---- Initialize components once per session ----
if "detector" not in st.session_state:
    try:
        with st.spinner("Loading models... (first run may download YOLO weights)"):
            st.session_state.detector = TruckDetector()
            st.session_state.classifier = TruckClassifier()
            st.session_state.calculator = MeasurementCalculator()
            st.session_state.visualizer = ImageVisualizer()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()

detector = st.session_state.detector
classifier = st.session_state.classifier
calculator = st.session_state.calculator
visualizer = st.session_state.visualizer

def cv2_to_pil(bgr_img: np.ndarray) -> Image.Image:
    """Convert OpenCV BGR image to PIL (RGB)."""
    if bgr_img is None:
        return None
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

if uploaded_file is not None:
    # Read and convert uploaded image
    try:
        pil_img = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(pil_img)  # RGB np array
        # OpenCV expects BGR; our visualizer draws in BGR
        bgr_img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        st.error(f"Error reading image: {e}")
        st.stop()

    # --- Automatic logo detection using template matching ---
    if logo_template_file is not None:
        try:
            logo_pil = Image.open(logo_template_file).convert("RGB")
            logo_np = np.array(logo_pil)
            logo_bgr = cv2.cvtColor(logo_np, cv2.COLOR_RGB2BGR)
            res = cv2.matchTemplate(bgr_img, logo_bgr, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            threshold = 0.6  # You can adjust this
            if max_val >= threshold:
                lx, ly = max_loc
                lw, lh = logo_bgr.shape[1], logo_bgr.shape[0]
                # Draw rectangle on detected logo
                cv2.rectangle(bgr_img, (lx, ly), (lx + lw, ly + lh), (0, 0, 255), 2)
                st.success(f"Logo detected at ({lx}, {ly}) with size {lw}x{lh} pixels. Confidence: {max_val:.2f}")
                # If truck detected, measure logo size in meters
                if 'pixels_per_meter' in locals():
                    logo_width_m = lw / pixels_per_meter
                    logo_height_m = lh / pixels_per_meter
                    st.caption(f"Logo size: {logo_width_m:.2f} m x {logo_height_m:.2f} m (auto-detected)")
            else:
                st.warning("Logo not confidently detected. Try a clearer template or adjust threshold.")
        except Exception as e:
            st.error(f"Error processing logo template: {e}")

    # Manual logo selection removed; use automatic template matching below

    # Detect trucks
    with st.spinner("Detecting truck..."):
        detections = detector.detect_trucks(bgr_img)  # works with either BGR/RGB for YOLO
        best = detector.get_best_detection(detections)

    if best is None:
        st.warning("No truck detected in this image. Try another image with a clearer side view.")
        st.image(pil_img, caption="Uploaded Image", use_column_width=True)
    else:
        x1, y1, x2, y2, conf = best
        width_px = max(1, x2 - x1)
        height_px = max(1, y2 - y1)

        # Classify truck type and nominal height (meters)
        truck_type, truck_height_m = classifier.classify(width_px, height_px)

        # For a quick demo, use the same truck box as ROI so you see numbers update
        roi = (x1, y1, width_px, height_px)
        width_m, height_m = calculator.calculate(roi, (x1, y1, x2, y2), truck_height_m)

        # Draw overlays
        vis = bgr_img.copy()
        visualizer.draw_truck_detection(vis, (x1, y1, x2, y2), truck_type, truck_height_m)
        visualizer.draw_measurements(vis, roi, (width_m, height_m))

        # Optional: add a 1m scale bar
        pixels_per_meter = (y2 - y1) / max(0.001, truck_height_m)
        visualizer.draw_scale_bar(vis, 1.0, pixels_per_meter, (50, 50))

        st.image(cv2_to_pil(vis),
                 caption=f"Detected: {truck_type}  •  Confidence: {conf:.2f}",
                 use_column_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Truck Type", truck_type)
        col2.metric("Width", f"{width_m:.2f} m")
        col3.metric("Height", f"{height_m:.2f} m")

        area_m2 = width_m * height_m
        st.caption(f"Approx area: {area_m2:.3f} m²")

    # Logo measurement now handled by template matching above
else:
    st.info("⬆️ Upload a JPG/PNG to get started.")
