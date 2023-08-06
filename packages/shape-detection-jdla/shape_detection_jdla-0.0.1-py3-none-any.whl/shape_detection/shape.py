import math


class Point(tuple):
    """Extends 'tuple', Point represents a 2d position."""
    def __new__(cls, x: int, y: int) -> tuple:
        return tuple.__new__(cls, (x, y))

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """X coordinate value."""
        return self._x

    @property
    def y(self) -> int:
        """Y coordinate value."""
        return self._y

    def __str__(self) -> str:
        return(f"({self.x}, {self.y})")


def get_distance(point_a: Point, point_b: Point) -> float:
    """Get the distance between two points.

    Args:
        point_a (Point): start point.
        point_b (Point): end point.

    Returns:
        float: Distance.

    Notes:
        See https://www.mathsisfun.com/algebra/distance-2-points.html for more info.
    """

    distance = math.sqrt(
        (math.pow((point_a.x-point_b.x), 2) + math.pow((point_a.y-point_b.y), 2)))
    return distance


def value_approximation(value_a: float, value_b: float, value_threshold: float) -> bool:
    """Compare two numbers to check if they are roughly the same.

    Args:
        value_a (float): First number.
        value_b (float): Second number.
        value_threshold (float): Approximation threshold.

    Returns: 
        bool: Whether or not the numbers are the same.
    """
    position = round(value_a/float(value_b), 1)
    flag = True if position >= (
        1-value_threshold) and position <= (1+value_threshold) else False
    return flag
