import os
import pygame


def _load_image(relative_image_path, colorkey=False):
    """ Utility method to load the images. It handles if the images contain
    transparency, and relative paths.
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    absolute_image_path = os.path.join(current_path, relative_image_path)

    image = pygame.image.load(absolute_image_path)
    return image
