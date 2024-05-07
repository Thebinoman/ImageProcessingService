"""Module for Image Processing"""
import os
import random
from pathlib import Path
from matplotlib.image import imread
import PIL.Image


class Img:
    """
    For Image Processing
    Load image on init, and run methods to add effects.
    Save the image to a file with save_img()
    """

    def __init__(self, path):
        """
        Load RGB image on initiation
        """

        self.path = Path(path)
        self.data = imread(path).tolist()

    def save_img(self):
        """
        Saves the image as a file by the path in self.path,
        with '_filtered' added to the name of the file.
        """

        # PIL.Image is used because matplotlib.image.imsave does not seem to work on RGB images

        # File destination path
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)

        # Create a new blank image with the same dimensions as your matrix
        width, height = len(self.data[0]), len(self.data)
        image = PIL.Image.new("RGB", (width, height))

        # Set the pixel values from your matrix
        for y in range(height):
            for x in range(width):
                r, g, b = self.data[y][x]
                image.putpixel((x, y), (r, g, b))

        # Save the image to a file
        image.save(new_path)

        #return the path of the saved file
        return new_path

    def delete(self):
        """
        Delete the image file
        """

        try:
            os.remove(self.path)
            return True

        except OSError as error:
            print(f'File deletion failed. Error: {error}')
            return error

    def blur(self, blur_level=16):
        """
        Blurs the image
        :param blur_level: The strength of the blur effect.
        The higher the value, the strongest the effect
        and longer the time to process: positive integer.
        :return:
        """

        # pylint: disable=R0914
        result = []
        for i in range(len(self.data) - blur_level + 1):
            row_result = []
            for j in range(len(self.data[0]) - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]

                # Iterate through the sub_matrix
                sum_r, sum_g, sum_b = 0, 0, 0
                total_pixels = 0

                # Iterate through each pixel
                for row in sub_matrix:
                    for pixel in row:
                        r, g, b = pixel
                        sum_r += r
                        sum_g += g
                        sum_b += b
                        total_pixels += 1

                # Calculate the average RGB values
                average_r = sum_r // total_pixels
                average_g = sum_g // total_pixels
                average_b = sum_b // total_pixels

                # average_b = sum(sum(sub_row[:, 2]) for sub_row in sub_matrix) // filter_sum
                row_result.append([average_r, average_g, average_b])
            result.append(row_result)

        self.data = result
        # pylint: enable=R0914

    def contour(self):
        """
        Contour effect
        """

        # Iterate over the rows in the matrix
        for i, row in enumerate(self.data):
            result = []
            # Iterate over the pixels in the row
            # Start from index 1, and looking back at the previous pixel
            for j in range(1, len(row)):
                # Calculating the average value of the RGB values
                # in the current and previous pixel
                # then, Collecting the difference between the
                # current pixel average and the previous average
                result.append([abs(sum(row[j-1]) - sum(row[j])) // 3] * 3)

            self.data[i] = result

    def rotate(self, angle = 90):
        """
        Rotates the image clockwise
        """

        # rotate twice for 180 degrees
        if angle == 180:
            self.rotate()
        # rotate 3 times for 270/-90  degrees
        elif angle in (-90, 270):
            self.rotate()
            self.rotate()

        # Transpose the Matrix
        transposed_mat = list(zip(*self.data))
        # Reverse each row of the transposed matrix
        self.data = [list(reversed(row)) for row in transposed_mat]

    def salt_n_pepper(self, strength = 0.2, salt = (255, 255, 255), pepper = (0, 0, 0)):
        """
        Adds Salt and Pepper effect to the image

        :param strength: How strong the effect will be: float between 0 - 0.5.
        :param salt: The color of the Salt: list or tuple of 3 integers
        with the value of 0 - 255. Default is white.
        :param pepper: The color of the pepper: list or tuple of 3 integers
        with the value of 0 - 255. Default is black.
        """

        # Iterate over all the pixel, with y as the index of the row
        # and x for the index of the pixel in the row
        for y, row in enumerate(self.data):
            for x, _ in enumerate(row):
                # random value between 0 - 1
                rand_val = random.random()
                # if the random value is smaller than strength,
                # turn the pixel to the color of 'salt'
                if rand_val < strength:
                    self.data[y][x] = salt
                # if the random value is bigger than 1 - strength,
                # turn the pixel to the color of 'pepper'
                elif rand_val > 1 - strength:
                    self.data[y][x] = pepper

    def color_noise(self, strength = 0.2):
        """
        Adds colorful noise to the image

        :param strength: How strong the effect will be: float between 0 - 0.5.
        """

        # Iterate over each color channel, in all the pixel,
        # with y as the index of the row,
        for y, row in enumerate(self.data):
            # x for the index of the pixel in the row,
            for x, pixel in enumerate(row):
                # and ci as the index of the channel
                for c, _ in enumerate(pixel):
                    # random value between 0 - 1
                    rand_val = random.random()
                    # if the random value is smaller than strength,
                    # turn this channel to be fully lit
                    if rand_val < strength:
                        self.data[y][x][c] = 255
                    # if the random value is bigger than 1 - strength,
                    # turn this channel to be fully off
                    elif rand_val > 1 - strength:
                        self.data[y][x][c] = 0

    def segment(self, threshold = 100, black = (0, 0, 0), white = (255, 255, 255)):
        """
        Some sort of "black and white" effect

        :param threshold: The threshold that separates between black and white:
        integer between 0 - 255. Default is 100.
        :param black: The color set to be black: list or tuple of 3 integers
        with the value of 0 - 255. Default is black.
        :param white: The color set to be white: list or tuple of 3 integers
        with the value of 0 - 255. Default is white.
        :return:
        """

        # Work with the sum of each pixel instead of average,
        # to save calculations, so threshold is multiplied by 3
        # instead of the sum divided by 3 each pixel
        threshold *= 3

        # Iterate over all the pixel, with y as the index of the row
        # and x for the index of the pixel in the row
        for y, row in enumerate(self.data):
            for x, pixel in enumerate(row):
                # if the average of a pixel is above the threshold,
                # it will turn white, otherwise it will turn black
                self.data[y][x] = white if sum(pixel) > threshold else black

    def concat(self, other_img, direction='horizontal', bg_color = (255, 255, 255)):
        """
        Adds a second image next to the current image, horizontally or vertically

        :param other_img: The second image to be added: instance of Img class
        :param direction: The direction to concat the image: 'horizontal' or 'vertical'.
        'horizontal' is default.
        :param bg_color: The color of the pixels that the images do not cover:
        list or tuple of 3 integers with the value of 0 - 255. Default is white.
        """

        if direction == 'horizontal':
            # Resize the two images to match each other height
            if len(self.data) < len(other_img.data):
                self.canvas_resize(len(self.data[0]), len(other_img.data), bg_color)
            elif len(other_img.data) < len(self.data):
                # set "other_img" to a new deep copy, so the original data will not be altered
                other_img = Img(other_img.path)
                other_img.canvas_resize(len(other_img.data[0]), len(self.data), bg_color)

            # Join the rows of both images
            for ri, row in enumerate(self.data):
                self.data[ri] = row + other_img.data[ri]

        elif direction == 'vertical':
            # Resize the two images to match each other width
            if len(self.data[0]) < len(other_img.data[0]):
                self.canvas_resize(len(other_img.data[0]), len(self.data), bg_color)
            elif len(other_img.data[0]) < len(self.data[0]):
                # set "other_img" to a new deep copy, so the original data will not be altered
                other_img = Img(other_img.path)
                other_img.canvas_resize(len(self.data[0]), len(other_img.data), bg_color)

            # Append the rows of the second image after the first
            self.data = self.data + other_img.data

    def grayscale(self):
        """
        Turns the image to be in the shades of gray.
        """

        # Iterate over all rows of the matrix
        for ri, row in enumerate(self.data):
            # Iterate over each pixel in the row
            for ci, pixel in enumerate(row):
                # Setting a value of grayscale according to the RGB values,
                # and setting the same grayscale value for each channel
                self.data[ri][ci] = [int(0.2989 * pixel[0] + 0.5870
                                     * pixel[1] + 0.1140 * pixel[2])] * 3

    def canvas_resize(self, width, height, bg_color = (255, 255, 255)):
        """
        Enlarge or crop the canvas of the image

        :param width: Width to resize in pixels: positive integer.
        :param height: Height to resize in pixels: positive integer.
        :param bg_color: The color of the pixels that the images do not cover:
        list or tuple of 3 integers with the value of 0 - 255. Default is white.
        :return:
        """

        # if cropping the height of the image
        if len(self.data) > height:
            # Slicing the rows of the matrix according to the value of 'height'
            self.data = self.data[:height]
        # if enlarging the height of the image
        elif len(self.data) < height:
            # appending rows at the length of self.data[0], with the value of 'bg_color'
            self.data = self.data + ([[bg_color] * len(self.data[0])] * (height - len(self.data)))

        # If cropping the width of the image
        if len(self.data[0]) > width:
            # Slicing each row of the matrix to the value of 'width'
            for ri, row in enumerate(self.data):
                self.data[ri] = row[:width]
        # If enlarging the width of the image
        elif len(self.data[0]) < width:
            # Adding the missing pixels at the end of each row to the length of 'width;
            for ri, row in enumerate(self.data):
                self.data[ri] = row + [bg_color] * (width - len(row))

    def rgb_posterize(self, threshold = 100):
        """
        Posterize effect in the combination of full (255) and empty (0)
        Red, Green and Blue values, according to the threshold.

        :param threshold: The threshold that separates between
        empty (0 value) and white (255 value) of each channel, of each pixel:
        integer between 0 - 255. Default is 100.
        """

        # Iterate over each channel in each pixel in the matrix
        # where y is the index of the row
        for y, row in enumerate(self.data):
            # x is the index of the pixel in the row
            for x, pixel in enumerate(row):
                # ci is the index of the channel
                for ci, channel in enumerate(pixel):
                    # if the value of the channel is larger than the threshold,
                    # it will set to full (255). Otherwise, it will set to empty (0)
                    self.data[y][x][ci] = 255 if channel > threshold else 0

    def multiply(self, other_img):
        """
        Multiplies the color between two images.
        It blends the dark parts of the second image on top of the other.

        :param other_img: The second image to be added: instance of Img class
        """

        # set "other_img" to a new deep copy, so the original data will not be altered
        other_img = Img(other_img.path)

        height = max(len(self.data), len(other_img.data))
        width = max(len(self.data[0]), len(other_img.data[0]))

        self.canvas_resize(width, height)
        other_img.canvas_resize(width, height)

        for y, row in enumerate(self.data):
            # x is the index of the pixel in the row
            for x, pixel in enumerate(row):
                # ci is the index of the channel
                for ci, channel in enumerate(pixel):
                    self.data[y][x][ci] = channel * other_img.data[y][x][ci] // 255
