"""
Setup script for Truck Measurement System
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    """Read README.md file"""
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Truck Logo/Design Measurement System"

# Read requirements
def read_requirements():
    """Read requirements.txt file"""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "ultralytics>=8.0.0",
            "opencv-python>=4.5.0",
            "numpy>=1.21.0",
            "requests>=2.25.0",
        ]

setup(
    name="truck-measurement-system",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A computer vision system for measuring objects on trucks",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/truck-measurement-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
        "web": [
            "streamlit>=1.28.0",
            "pillow>=8.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "truck-measurement=truck_measurement.main:main",
            "truck-measurement-web=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "truck_measurement": ["*.py"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/truck-measurement-system/issues",
        "Source": "https://github.com/yourusername/truck-measurement-system",
        "Documentation": "https://github.com/yourusername/truck-measurement-system/docs",
    },
)