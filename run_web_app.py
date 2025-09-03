#!/usr/bin/env python3
"""
Easy launcher script for the Truck Measurement Web App

This script helps users launch the Streamlit web interface easily
without needing to remember the streamlit command.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'opencv-python', 
        'ultralytics',
        'numpy',
        'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install missing requirements"""
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print("Please install manually: pip install -r requirements.txt")
        return False

def launch_app():
    """Launch the Streamlit app"""
    print("🚀 Launching Truck Measurement Web App...")
    print("📱 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Launch streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down the server...")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install requirements first.")
        return False
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚛 TRUCK MEASUREMENT SYSTEM - WEB LAUNCHER")
    print("=" * 50)
    
    # Check if app.py exists
    if not Path("app.py").exists():
        print("❌ app.py not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print(f"⚠️  Missing required packages: {', '.join(missing)}")
        print("📦 Attempting to install...")
        
        if not install_requirements():
            return
        
        # Check again after installation
        missing = check_requirements()
        if missing:
            print(f"❌ Still missing packages: {', '.join(missing)}")
            print("Please install manually and try again.")
            return
    
    print("✅ All requirements satisfied!")
    print()
    
    # Launch the