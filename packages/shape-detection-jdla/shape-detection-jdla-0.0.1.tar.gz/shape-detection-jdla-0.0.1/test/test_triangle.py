from shape_detection.triangle import Triangle
from shape_detection import shape
import unittest

# Run file: python -m test.test_triangle


class TestTriangle(unittest.TestCase):
    def test_triangle(self):
        # Test points
        point_a = shape.Point(1, 1)
        point_b = shape.Point(1, 2)
        point_c = shape.Point(3, 1)

        # Test triangle
        triangle = Triangle(point_a, point_b, point_c)

        print(triangle.side_a, triangle.side_b, triangle.side_c)

        self.assertAlmostEqual(triangle.angle_a, 90)
        self.assertAlmostEqual(triangle.angle_b, 63.43494882292201)
        self.assertAlmostEqual(triangle.angle_c, 26.565051177077994)

        self.assertAlmostEqual(triangle.side_a, 2.23606797749979)
        self.assertAlmostEqual(triangle.side_b, 2)
        self.assertAlmostEqual(triangle.side_c, 1)


if __name__ == "__main__":
    unittest.main()
