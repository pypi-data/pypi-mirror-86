# Shape detection with OpenCV

Shape detection using OpenCV

## Overview

This python module is part of a Rubik's Cube solver I’m working on. The initial challenge is to create a reliable shape detection module that can track the Rubik's cube faces and filter the squares to solve the puzzle.

We will skip the canny edge detection because the [CVTools](https://github.com/JosueDLA/CVTools) module take care of that problem for us, once we have the contours we need to get an approximation and decide if a given contour is a square, for this we have some rules:

- There must be four corners
- All four lines must be the same length
- All four corners must be 90°
- Lines AB and CD must be horizontal lines
- Lines AC and BC must be vertical lines
- The contour must be concave

## Instalation

Install this package

```bash
pip install shape-detection-jdla
```

Clone this repository

```bash
git clone https://github.com/JosueDLA/ShapeDetection
```

Install requirements.txt

```bash
pip install requirements.txt
```

## Software and Tools Used

- OpenCV
- NumPy

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

This project is heavily inspired by [@dwalton76](https://github.com/dwalton76) [rubiks color resolver](https://github.com/dwalton76/rubiks-color-resolver)

## References

- [OpenCV Shape detection](https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/)

- [OpenCV: Contour Hierarchy](https://docs.opencv.org/3.1.0/d9/d8b/tutorial_py_contours_hierarchy.html)

- [OpenCV: Contour Features](https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html)

- [LEGO Mindstorms Project](http://programmablebrick.blogspot.com/2017/02/rubiks-cube-tracker-using-opencv.html)

- [Finding Extreme Points in Contour with OpenCV](https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/)

- [Sorting Contours using Python and OpenCV](https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/)
