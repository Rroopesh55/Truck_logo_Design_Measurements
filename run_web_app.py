import subprocess
import sys
import os


REQUIRED_PACKAGES = ["streamlit", "ultralytics", "opencv-python", "numpy", "Pillow"]


def install_requirements():
for package in REQUIRED_PACKAGES:
try:
__import__(package.split("==")[0])
except ImportError:
print(f"Installing {package}...")
subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
install_requirements()
print("Launching Streamlit App...")
os.system("streamlit run app.py")