"""
Test Rotate Function
"""

import unittest
# pylint: disable=E0401
from polybot.img_proc import Img
# pylint: enable=E0401


IMG_PATH = '../../.img/beatles.jpeg'


class TestImgRotate(unittest.TestCase):
    """
    Test Concat Class
    """

    def setUp(self):
        """
        Test Setup
        """

        self.img = Img(IMG_PATH)
        self.original_dimension = (len(self.img.data), len(self.img.data[0]))

    def test_rotation_dimension(self):
        """
        Test Rotate Dimension
        """

        self.img.rotate()
        actual_dimension = (len(self.img.data), len(self.img.data[0]))
        self.assertEqual(self.original_dimension, actual_dimension[::-1])

    def test_360_rotation(self):
        """
        Test 360 Rotation
        Output result should be identical to the input image
        """

        self.img.rotate()
        self.img.rotate()
        self.img.rotate()
        self.img.rotate()

        rotated_image = [row[::-1] for row in self.img.data]
        expected_img = [row[::-1] for row in rotated_image]

        self.assertEqual(expected_img, self.img.data)


if __name__ == '__main__':
    unittest.main()
