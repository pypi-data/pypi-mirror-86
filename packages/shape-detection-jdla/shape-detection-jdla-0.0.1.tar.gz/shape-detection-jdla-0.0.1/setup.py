"""
# Color Thief

A module for detecting shapes using OpenCV.

Installation

```bash
pip install shape-detection-jdla
```

# Overview

Square detection rules:

- There must be four corners
- All four lines must be the same length
- All four corners must be 90°
- Lines AB and CD must be horizontal lines
- Lines AC and BC must be vertical lines
- The contour must be concave

# Example


```python
from shape_detection.square import Square
import numpy as np

try:
    contour = np.array([[[368, 160]], [[391, 163]],
                        [[384, 200]], [[361, 194]]])

    square = Square.is_square(contour)

    print(square)

except Exception as e:
    print(e)
```

# Links
* [github](https://github.com/JosueDLA/ShapeDetection)

"""

from setuptools import find_packages
from setuptools import setup

setup(
    name="shape-detection-jdla",
    version="0.0.1",
    py_modules=["shape_detection"],
    description="Shape detection using OpenCV",
    long_description_content_type="text/markdown",
    long_description=__doc__,
    author="Josué de León",
    author_email="josuedlavs@gmail.com",
    url="https://github.com/JosueDLA/ShapeDetection",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "numpy==1.19.2",
        "opencv-python==4.4.0.44",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
