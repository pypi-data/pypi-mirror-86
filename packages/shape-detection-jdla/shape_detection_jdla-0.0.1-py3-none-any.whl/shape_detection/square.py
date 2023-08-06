from __future__ import annotations
from .triangle import Triangle
from .shape import Point
from . import shape
import numpy as np
import cv2

RIGHT_ANGLE = 90


class Square:
    """Four-sided poligon.\n
    A______B  \r
    |      |  \r
    |      |  \r
    D______C  \r
    """

    """
    box_threshold (float): Approximation threshold.
    line_threshold (float, optional): Line size threshold. 
    angle_threshold (float, optional): Angle threshold. 
    size_threshold (float, optional): Point position threshold
    min_area (float, optional): Minimal area threshold.
    arc_threshold (float, optional): Contour arc threshold.
    """
    box_threshold = 0.40
    line_threshold = 0.30
    size_threshold = 0.20
    angle_threshold = 0.20
    arc_threshold = 0.05
    min_area = 300

    def __init__(self, point_a: Point, point_b: Point, point_c: Point, point_d: Point, array: np.ndarray = []):
        """Square formed by four given points."""
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.point_d = point_d
        self.array = array

    def __str__(self) -> str:
        return (f"{self.point_a} {self.point_b} {self.point_c} {self.point_d}")

    @property
    def angle_a(self) -> float:
        """Angle A°."""
        return Triangle.get_angle(self.point_a, self.point_b, self.point_d)

    @property
    def angle_b(self) -> float:
        """Angle B°."""
        return Triangle.get_angle(self.point_b, self.point_c, self.point_a)

    @property
    def angle_c(self) -> float:
        """Angle C°."""
        return Triangle.get_angle(self.point_c, self.point_d, self.point_b)

    @property
    def angle_d(self) -> float:
        """Angle D°."""
        return Triangle.get_angle(self.point_d, self.point_a, self.point_c)

    @property
    def line_ab(self) -> float:
        """Line AB length."""
        return shape.get_distance(self.point_a, self.point_b)

    @property
    def line_bc(self) -> float:
        """Line BC length."""
        return shape.get_distance(self.point_b, self.point_c)

    @property
    def line_cd(self) -> float:
        """Line CD length."""
        return shape.get_distance(self.point_c, self.point_d)

    @property
    def line_ad(self) -> float:
        """Line AD length."""
        return shape.get_distance(self.point_a, self.point_d)

    @classmethod
    def _size_approximation(cls, contour: np.ndarray) -> bool:
        """Compare the size of a bound contour to the contour.

        Args:
            contour (np.ndarray): OpenCV contour.

        Returns: 
            bool: Whether or not the contours are the same size.

        Notes: See https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/ for  more info.
        """
        (_, _, w, h) = cv2.boundingRect(contour)
        area = w / float(h)
        flag = True if area >= (
            1 - cls.box_threshold) and area <= (1+cls.box_threshold) else False
        return flag

    @classmethod
    def _line_approximation(cls, square: Square) -> bool:
        """Compare the size of 4 lines to check if they are the same length.

        Args:
            square (Square): Square object.

        Returns:
            bool: Whether or not the lines are the same length.
        """

        average = (square.line_ab + square.line_bc +
                   square.line_cd + square.line_ad)/4

        flag1 = shape.value_approximation(
            square.line_ab, average, value_threshold=cls.line_threshold)
        flag2 = shape.value_approximation(
            square.line_bc, average, value_threshold=cls.line_threshold)
        flag3 = shape.value_approximation(
            square.line_cd, average, value_threshold=cls.line_threshold)
        flag4 = shape.value_approximation(
            square.line_ad, average, value_threshold=cls.line_threshold)

        return True if flag1 and flag2 and flag3 and flag4 else False

    @classmethod
    def _angle_approximation(cls, square: Square) -> bool:
        """ Get the four angles of a square and check if they are roughly the same.

        Args:
            square (Square): Square object.

        Returns:
            bool: Whether or not the angles are the same.
        """

        flag1 = shape.value_approximation(
            square.angle_a, RIGHT_ANGLE, value_threshold=cls.angle_threshold)
        flag2 = shape.value_approximation(
            square.angle_b, RIGHT_ANGLE, value_threshold=cls.angle_threshold)
        flag3 = shape.value_approximation(
            square.angle_c, RIGHT_ANGLE, value_threshold=cls.angle_threshold)
        flag4 = shape.value_approximation(
            square.angle_d, RIGHT_ANGLE, value_threshold=cls.angle_threshold)

        if(flag1 and flag2 and flag3 and flag4):
            return True
        else:
            return False

    @classmethod
    def is_square(cls, contour: np.ndarray) -> Square:
        """Find if a contour is a square.

        Rules:
            1 - There must be four corners.
            2 - All four lines must be the same length.
            3 - All four corners must be 90°.
            4 - AB and CD must be horizontal lines.
            5 - AC and BC must be vertical lines.
            6 - The contour must be concave.

        Args: 
            contour (np.ndarray): OpenCV contour.

        Returns:
            Square: Square object.
        """

        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(
            contour, cls.arc_threshold*perimeter, True)

        rect = cv2.minAreaRect(approximation)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        if (len(approximation) != 4):
            # Poligon has 4 courners
            raise Exception("Square must have four corners.")
        if not cls._size_approximation(approximation):
            # Size Approximation
            raise Exception("Bound and contour must be the same size.")
        if cv2.contourArea(approximation) < cls.min_area:
            # Min Area
            raise Exception("Minimum area required is not met.")

        # Sort corner of square
        corners = [tuple(approximation[0][0]), tuple(approximation[1][0]),
                   tuple(approximation[2][0]), tuple(approximation[3][0])]
        corners.sort(key=lambda p: p[1])

        top_points = corners[2:]
        buttom_points = corners[:2]

        top_points.sort(key=lambda p: p[0])
        buttom_points.sort(key=lambda p: p[0], reverse=True)

        corners = top_points + buttom_points

        point_a = shape.Point(corners[0][0], corners[0][1])
        point_b = shape.Point(corners[1][0], corners[1][1])
        point_c = shape.Point(corners[2][0], corners[2][1])
        point_d = shape.Point(corners[3][0], corners[3][1])

        square = Square(point_a, point_b, point_c, point_d, approximation)

        if not shape.value_approximation(square.line_ab, square.line_cd, value_threshold=cls.size_threshold):
            # Is Horizontal
            raise Exception("Line AB, and CD must be horizontal.")
        if not shape.value_approximation(square.line_ad, square.line_bc, value_threshold=cls.size_threshold):
            # Is Vertical
            raise Exception("Line AD, and BC must be vertical.")
        if not cls._line_approximation(square):
            # Lines Same Length
            raise Exception("All lines in the square must be the same length.")
        if not cls._angle_approximation(square):
            # Right Angle
            raise Exception("All angles in the square must be 90°.")
        return square
