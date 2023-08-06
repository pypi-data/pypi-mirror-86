from shape_detection.square import Square
from shape_detection import shape
import numpy as np
import unittest

# Run file: python -m test.test_square


class TestSquare(unittest.TestCase):
    def test_square_a(self):
        # Test points
        point_a = shape.Point(-4, -1)
        point_b = shape.Point(-1, -1)
        point_c = shape.Point(-1, -4)
        point_d = shape.Point(-4, -4)

        # Test Square
        square = Square(point_a, point_b, point_c, point_d)

        self.assertAlmostEqual(square.angle_a, 90)
        self.assertAlmostEqual(square.angle_b, 90)
        self.assertAlmostEqual(square.angle_c, 90)
        self.assertAlmostEqual(square.angle_d, 90)

        self.assertAlmostEqual(square.line_ab, 3)
        self.assertAlmostEqual(square.line_bc, 3)
        self.assertAlmostEqual(square.line_cd, 3)
        self.assertAlmostEqual(square.line_ad, 3)

    def test_square_b(self):
        # Test points
        point_a = shape.Point(1, 7)
        point_b = shape.Point(4, 2)
        point_c = shape.Point(-1, -1)
        point_d = shape.Point(-4, 4)

        # Test Square
        square = Square(point_a, point_b, point_c, point_d)

        self.assertAlmostEqual(square.angle_a, 90)
        self.assertAlmostEqual(square.angle_b, 90)
        self.assertAlmostEqual(square.angle_c, 90)
        self.assertAlmostEqual(square.angle_d, 90)

        self.assertAlmostEqual(square.line_ab, 5.830951894845301)
        self.assertAlmostEqual(square.line_bc, 5.830951894845301)
        self.assertAlmostEqual(square.line_cd, 5.830951894845301)
        self.assertAlmostEqual(square.line_ad, 5.830951894845301)

    def test_square_c(self):
        # Test points
        point_a = shape.Point(1, 3)
        point_b = shape.Point(3, 3)
        point_c = shape.Point(3, 1)
        point_d = shape.Point(1, 1)

        # Test Square
        square = Square(point_a, point_b, point_c, point_d)

        self.assertAlmostEqual(square.angle_a, 90)
        self.assertAlmostEqual(square.angle_b, 90)
        self.assertAlmostEqual(square.angle_c, 90)
        self.assertAlmostEqual(square.angle_d, 90)

        self.assertAlmostEqual(square.line_ab, 2)
        self.assertAlmostEqual(square.line_bc, 2)
        self.assertAlmostEqual(square.line_cd, 2)
        self.assertAlmostEqual(square.line_ad, 2)

    def test_is_square(self):
        # Test Contour
        contour_good = np.array([[[368, 160]], [[391, 163]],
                                 [[384, 200]], [[361, 194]]])

        contour_bad = np.array([[[246, 100]], [[247, 99]],
                                [[248, 100]], [[247, 101]]])

        self.assertIsInstance(Square.is_square(contour_good), Square)
        self.assertRaises(Exception, Square.is_square, contour_bad)


if __name__ == "__main__":
    unittest.main()
