from shape_detection.shape import Point
from shape_detection import shape
import unittest

# Run file: python -m test.test_shape


class TestShape(unittest.TestCase):
    def test_point(self):
        # Test point
        point = Point(1, 2)

        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)
        self.assertEqual(point, (1, 2))

    def test_get_distance(self):
        # Test points
        point_a = shape.Point(1, 2)
        point_b = shape.Point(3, 1)

        distance = shape.get_distance(point_a, point_b)

        self.assertAlmostEqual(distance, 2.236067977)

    def test_value_approximation(self):
        # Test value
        upper = 1.1
        mid = 1
        lower = 0.9

        approx_a = shape.value_approximation(upper, mid, 0.10)
        approx_b = shape.value_approximation(mid, lower, 0.10)
        approx_c = shape.value_approximation(upper, lower, 0.10)
        approx_d = shape.value_approximation(mid, upper, 0.10)
        approx_e = shape.value_approximation(lower, mid, 0.10)
        approx_f = shape.value_approximation(lower, upper, 0.10)

        self.assertTrue(approx_a)
        self.assertTrue(approx_b)
        self.assertFalse(approx_c)
        self.assertTrue(approx_d)
        self.assertTrue(approx_e)
        self.assertFalse(approx_f)


if __name__ == "__main__":
    unittest.main()
