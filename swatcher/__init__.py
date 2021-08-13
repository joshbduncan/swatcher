# -*- coding: utf-8 -*-
"""
    Swatcher
    --------
    A Python module for generating Adobe ASE color swatches from images.
    
    :copyright: (c) 2021 Josh Duncan.
    :license: MIT, see LICENSE for more details.
"""

__version__ = "1.0.3"

import os

from datetime import datetime
from PIL import Image
from . import color, export, image, palette


def get_file_info(file: object) -> tuple:
    """
    Check to see if the provided image was a file path or a file object.

    :param colors: PIL Image object
    :returns: file path
    """
    fp = getattr(file, "filename", None)
    if not fp:  # if a file object was provided
        home = os.path.expanduser("~")
        created_dt = datetime.now().replace(microsecond=0).isoformat().replace(":", "")
        filename = created_dt
        fp = os.path.join(home, filename)
    return fp


def validate_path(path: str):
    """Check for existance of export path."""
    dp = os.path.dirname(path)
    if not os.path.exists(dp):
        raise FileNotFoundError("Sorry, the save location doesn't exist.")


class Swatcher:
    """
    This class represents a Swatcher object used for sampling colors
    from an image and exporting them as Adobe ASE color swatches.
    """

    def __init__(self, file, max_colors: int = None, sensitivity: int = None):
        """
        Initialize an image for color sampling.

        :param `file`: a filename (string) or file object in binary mode
        """
        self.image = Image.open(file)
        self._max_colors = 8
        self._sensitivity = 75
        self._palette = None
        self._palette_image = None
        # get or set the file path
        self.path = get_file_info(self.image)
        # process image for color sampling
        self._processed_image = image.process_image(self.image)
        # count and sort colors from every pixel
        self._colors = color.get_colors(self._processed_image)
        # sample the image
        self.sample(max_colors, sensitivity)

    @property
    def palette(self) -> list:
        """
        Most present colors from `self.image` using the current
        sample settigs `self.max_colors` and `self.sensitivity`.

        :returns: list of rgb color tuples
        """
        if not self._palette:
            self.sample(self._max_colors, self._sensitivity)
        return self._palette

    @property
    def max_colors(self) -> int:
        """Maximum colors to return during sampling."""
        return self._max_colors

    @max_colors.setter
    def max_colors(self, value: int):
        if type(value) != int:
            raise TypeError("Max Colors must be an integer.")
        elif not 1 <= value <= 20:
            raise ValueError("Max Colors must be an integer between 1 and 20.")
        self._max_colors = value
        self._reset_current_palette()

    @property
    def sensitivity(self) -> int:
        """
        How perceptively different (Euclidean Distance) a color
        must be from others to be included in the sampled palette.
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value: int):
        if type(value) != int:
            raise TypeError("Sensitivity must be an integer.")
        elif not 0 <= value <= 250:
            raise ValueError("Sensitivity must be an integer between 0 and 250.")
        self._sensitivity = value
        self._reset_current_palette()

    @property
    def processed_image(self):
        """Processed `self.image` PIL image object."""
        return self._processed_image

    @property
    def palette_image(self) -> object:
        """
        PIL.Image object of currently sampled swatches.

        :returns: PIL Image object
        """
        if not self._palette_image:
            self._palette_image = palette.draw_swatches(self.palette)
        return self._palette_image

    def sample(self, max_colors: int = None, sensitivity: int = None) -> list:
        """
        Sample a new palette from `self.image` using the supplied sample
        settings `max_colors` and `sensitivity` or the defaults.

        :param max_colors: maximum colors to sample from `self.image`
        :param sensitivity: how perceptively different (Euclidean Distance) a color
                          must be from others to be included in the sampled palette.
        :returns: list of rgb color tuples
        """
        if max_colors:
            self.max_colors = max_colors
        if sensitivity or sensitivity == 0:
            self.sensitivity = sensitivity

        self._reset_current_palette()
        self._palette = palette.sample(
            self._colors, self._max_colors, self._sensitivity
        )
        return self.palette

    def show_processed_image(self):
        """Show `self.processed_image` in your standard image viewer."""
        self.processed_image.show()

    def show_palette_image(self):
        """Show `self.palette_image` in your standard image viewer."""
        self.palette_image.show()

    def export_ase_file(self, path: str = None) -> str:
        """
        Export an Adobe ASE (.ase) file of all swatches from `self.palette`.

        If no valid path is provided the file will be saved in
        the same directory as `self.image`.

        This operation will overwrite any files of the same name.

        :param `path`: a filename string
        :returns: file location
        :exception FileNotFoundError: If the save location doesn't exist
        """

        # check the export location final export location
        if path:
            validate_path(path)
        else:
            path = self.path

        exported_file = export.export_ase_file(self.palette, path)
        return exported_file

    def export_palette_image(self, path: str = None) -> str:
        """
        Export a PNG version of `self.palette_image`.

        If no valid path is provided the file will be saved in
        the same directory as `self.image`.

        This operation will overwrite any files of the same name.

        :param `path`: a filename string
        :returns: file location
        :exception FileNotFoundError: If the save location doesn't exist
        """

        # check the export location final export location
        if path:
            validate_path(path)
        else:
            path = self.path

        exported_file = export.export_image_file(self.palette_image, path)
        return exported_file

    def _reset_current_palette(self):
        """Reset instance palette after sample settings update."""
        self._palette = None
        self._palette_image = None

    def __repr__(self):
        return repr(
            f"Swatcher object: {self.path}, {self.max_colors=}, {self.sensitivity=}"
        )

    def __str__(self):
        return f"""Swatcher object:
File: {self.path}
Settings: max colors={self.max_colors}, sensitivity={self.sensitivity}
Sampled Colors: {self.palette}"""
