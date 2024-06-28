"""
Test Salt n Pepper
"""

import unittest
# pylint: disable=E0401
from polybot.img_proc import Img
# pylint: enable=E0401


IMG_PATH = '../../.img/beatles.jpeg'


class TestImgSaltNPepper(unittest.TestCase):
    """
    Test Salt n Pepper Class
    """

    @classmethod
    def setUpClass(cls):
        """
        Test Setup
        """

        cls.img = Img(IMG_PATH)
        cls.original_img = Img(IMG_PATH)

        cls.img.salt_n_pepper()

    def test_rotation_dimension(self):
        """
        Test resolution of the result
        """
        actual_dimension = (len(self.img.data), len(self.img.data[0]))
        expected_dimension = (len(self.original_img.data), len(self.original_img.data[0]))
        self.assertEqual(expected_dimension, actual_dimension)


if __name__ == '__main__':
    unittest.main()
