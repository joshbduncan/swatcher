# -*- coding: utf-8 -*-
"""
    Swatcher
    --------
    A Python module for generating Adobe ASE color swatches from images.
    
    :copyright: (c) 2021 Josh Duncan.
    :license: MIT, see LICENSE for more details.
"""

__version__ = "1.0.0"

import os

from datetime import datetime
from PIL import Image
from . import color, export, image, palette


def save_location(file: object) -> tuple:
    """
    Check to see if the provided image was a file path or a file object.

    :param colors: PIL Image object
    :returns: tuple (location, filename)
    """
    filepath = getattr(file, "filename", None)
    if filepath:  # if a path was provided we are set
        location = filepath
    else:  # if a file object was provided
        # get the users home directory
        home = os.path.expanduser("~")
        # get the current date and time
        created_dt = datetime.now().replace(microsecond=0).isoformat()
        # set a new save as filename
        filename = "Swatcher " + created_dt
        # set the final save location
        location = os.path.join(home, filename)
    return os.path.split(location)


class Swatcher:
    """
    This class represents a Swatcher object used for sampling colors
    from an image and exporting them as Adobe ASE color swatches.
    """

    def __init__(self, file):
        """
        Initialize an image for color sampling.

        :param `file`: a filename (string) or file object in binary mode
        """
        self.image = Image.open(file)
        # set save path and filename
        self._location, self._filename = save_location(self.image)
        # process image for color sampling
        self._processed_image = image.process_image(self.image)
        # count and sort colors from every pixel
        self._colors = color.get_colors(self._processed_image)
        # initialize other settings and variables
        self._max_colors = 8
        self._sensitivity = 75
        self._palette = None
        self._palette_image = None

    def sample(self, max_colors: int = None, sensitivity: int = None) -> list:
        """
        Resample a new palette from `self.image` using the
        supplied sample settings `max_colors` and `sensitivity`.

        :param max_colors: maximum colors to sample from `self.image`
        :param sensitivity: how perceptively different (Euclidean Distance) a color
                          must be from others to be included in the sampled palette.
        :returns: list of rgb color tuples
        """
        if max_colors:
            self.max_colors = max_colors
        if sensitivity:
            self.sensitivity = sensitivity
        return self.palette

    @property
    def palette(self) -> list:
        """
        Most present colors from `self.image` using the current
        sample settigs `self.max_colors` and `self.sensitivity`.

        :returns: list of rgb color tuples
        """
        if not self._palette:
            self._palette = palette.sample(
                self._colors, self.max_colors, self.sensitivity
            )
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

    def show_processed_image(self):
        """Show `self.processed_image` in your standard image viewer."""
        self.processed_image.show()

    def show_palette_image(self):
        """Show `self.palette_image` in your standard image viewer."""
        self.palette_image.show()

    def export_ase_file(self, location: str = None, filename: str = None):
        """
        Export an Adobe ASE (.ase) file of all swatches from `self.palette`.

        If no valid locaiton is provided the file will be saved in
        the same directory as `self.image`.

        If a filename is not provided, the file will be saved as
        the same name as `self.image`.

        This operation will overwrite any files of the same name.

        :param `location`: file system location where the ase file should be saved
        :param `filename`: filename to save the ASE file as
        :exception FileNotFoundError: If the save location doesn't exist
        """

        # set final export location
        location = self._check_export_location(location)
        # if filename not provided use filename of `self.image`
        if not filename:
            filename = self._filename

        # set the final export patha and save the file
        path = os.path.join(location, f"{filename}-SWATCHER.ase")
        exported_file = export.export_ase_file(self.palette, path)
        return exported_file

    def export_palette_image(self, location: str = None, filename: str = None):
        """
        Export a JPEG version of `self.palette_image`.

        If no valid locaiton is provided the file will be saved in
        the same directory as `self.image`.

        If a filename is not provided, the file will be saved as
        the same name as `self.image`.

        This operation will overwrite any files of the same name.

        :param `location`: file system location where the ase file should be saved
        :param `filename`: filename to save the ASE file as
        :exception FileNotFoundError: If the save location doesn't exist
        """

        # set final export location
        location = self._check_export_location(location)
        # if filename not provided use filename of `self.image`
        if not filename:
            filename = self._filename

        # set the final export patha and save the file
        path = os.path.join(location, f"{filename}-SWATCHER.jpg")
        exported_file = export.export_image_file(self.palette_image, path)
        return exported_file

    def _reset_current_palette(self):
        """Reset instance palette after sample settings update."""
        self._palette = None
        self._palette_image = None

    def _check_export_location(self, path):
        """Check for validity of provided export location."""
        if path and not os.path.exists(path):
            raise FileNotFoundError("Sorry, the save location doesn't exist.")
        else:  # set location to same as `self.image`
            path = self._location
        return path

    def __repr__(self):
        return repr(
            f"Swatcher object: {self._filename}, {self.max_colors=}, {self.sensitivity=}"
        )

    def __str__(self):
        return f"""Swatcher object:
File: {self._filename}
Settings: max colors={self.max_colors}, sensitivity={self.sensitivity}
Sampled Colors: {self.palette}"""
