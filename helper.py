'''
Helper functions for the puzzle.py
'''

import random
from simpleimage import SimpleImage
import math
import numpy as np

def create_solution(num_pieces, seed = 2000):
    '''
    Takes a number of pieces as input
    Returns the original order and a random order of pieces as a dictionary with 
    {orignal_position: {'random_position': random_position}}

    Number is by column then row like in
    ((0, 1, 2)
     (3, 4, 5)
     (6, 7, 8))

    >>> create_solution(4)
    {0: {'random_position': 2}, 1: {'random_position': 1}, 2: {'random_position': 0}, 3: {'random_position': 3}}
    
    >>> create_solution(2)
    {0: {'random_position': 0}, 1: {'random_position': 1}}
    '''
    correct_order = [i for i in range(num_pieces)]
    random_order = correct_order.copy()
    random.Random(seed).shuffle(random_order)
    temp = [(correct_order[i], random_order[i]) for i in range(0, len(correct_order))]
    solution = {}
    for a, b in temp:
        #solution.setdefault(a, []).append(b)
        solution.setdefault(a, {'random_position': b})

    return solution

def create_blank_pieces(num_pieces, piece_width, piece_height):
    '''
    Takes a number of pieces num_pieces and their width and height as input
    Returns a list of num_pieces of blank SimpleImages of given width and height
    '''
    puzzle_pieces = []
    for i in range(num_pieces):
        puzzle_pieces.append(SimpleImage.blank(piece_width, piece_height))
    return puzzle_pieces

def rotate_coordinates(x, y, angle, width, height):
    '''
    This takes coordinates of a pixel, the image's width and height as 
    input. It returns the coordinates of the image rotates by the given
    angle. (Pixel coordinates are always integers)
    NOTE: The angle has to be a integer multiple of 90 degrees.

    Helper function to rotate_image() and rotate_file().

    I wrote this function as an extension to SimpleImage so the 
    remaining programme can be based on it.

    It applies an affine transformation based on the matrix
    ((cos(angle), sin(angle), 0)
    (-sin(angle), cos(angle), 0)
    (0,         , 0         , 1))
    This rotates the image around the origin. Therefore the rotated
    image afterwards gets offset so that the lower left corner sits
    at the origin again.

    cf. https://stackabuse.com/affine-image-transformations-in-python-with-numpy-pillow-and-opencv/

    The Python Pillow library in contrast implements an 
    inverse transformation v,w = T^(-1)(x,y) with x, y as output pixels
    and v,w as input pixels.
    See https://github.com/python-pillow/Pillow/blob/master/src/PIL/Image.py
    I assume this is computationally more efficient.
    
    >>> rotate_coordinates(0, 0, 90, 60, 60)
    (0, 59)
    >>> rotate_coordinates(59, 59, 180, 60, 60)
    (0, 0)
    >>> rotate_coordinates(59, 0, 270, 60, 60)
    (59, 59)
    '''
    angle = angle % 360
    if angle == 0:
        offset = np.array([0, 0, 0])
    elif angle == 90:
        offset = np.array([0, height - 1, 0])
    elif angle == 180:
        offset = np.array([width - 1, height - 1, 0])
    elif angle == 270:
        offset = np.array([width - 1, 0, 0])
    else:
        raise ValueError('Angle is not an integer multiple of 90 degrees.')
    angle = math.radians(angle)
    matrix = np.array([[round(math.cos(angle), 15), round(math.sin(angle), 15), 0],
                       [-round(math.sin(angle), 15), round(math.cos(angle), 15), 0],
                       [0, 0, 1]])
    coord = np.array([x , y , 1])
    rotation = matrix @ coord
    rotation = rotation + offset
    x_rot, y_rot, i = rotation
    return int(x_rot), int(y_rot)

def rotate_image(original, angle):
    '''
    Rotates an image by angle and returns the rotated image.
    Requires an angle which is an integer multiple of 90 degrees.
    '''
    width = original.width
    height = original.height
    
    angle = angle % 360
    if angle == 90 or angle == 270:
        rotation = SimpleImage.blank(height, width)
    elif angle == 0 or angle == 180:
        rotation = SimpleImage.blank(width, height)
    else:
        raise ValueError('Angle is not an integer multiple of 90 degrees.')
    
    for pixel in original:
        x = pixel.x
        y = pixel.y
        x_rot, y_rot = rotate_coordinates(x, y, angle, width, height)
        rotation.set_pixel(x_rot, y_rot, pixel)
    return rotation

def rotate_file(filename, angle):
    '''
    File based implementation of rotate_image()
    '''
    original = SimpleImage(filename)
    width = original.width
    height = original.height
    
    angle = angle % 360
    if angle == 90 or angle == 270:
        rotation = SimpleImage.blank(height, width)
    elif angle == 0 or angle == 180:
        rotation = SimpleImage.blank(width, height)
    else:
        raise ValueError('Angle is not an integer multiple of 90 degrees.')
    
    for pixel in original:
        x = pixel.x
        y = pixel.y
        x_rot, y_rot = rotate_coordinates(x, y, angle, width, height)
        rotation.set_pixel(x_rot, y_rot, pixel)
    return original, rotation

if __name__ == '__main__':
    import doctest
    doctest.testmod()

