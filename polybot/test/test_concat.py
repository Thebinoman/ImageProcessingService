"""
Test Concat Function
"""

import unittest
# pylint: disable=E0401
from polybot.img_proc import Img
# pylint: enable=E0401

IMG_PATH = '../../.img/beatles.jpeg'


class TestImgConcat(unittest.TestCase):
    """
    Test Concat Class
    """

    @classmethod
    def setUpClass(cls):
        cls.img = Img(IMG_PATH)
        cls.other_img = Img(IMG_PATH)
        cls.img.concat(cls.other_img)

    def test_concat_result_dimension(self):
        """
        Test resolution of result of concat
        """
        actual_height = len(self.img.data)
        actual_width = len(self.img.data[0])

        expected_height = len(self.other_img.data)
        expected_width = 2 * len(self.other_img.data[0])

        self.assertEqual(actual_height, expected_height)
        self.assertEqual(actual_width, expected_width)


if __name__ == '__main__':
    unittest.main()
