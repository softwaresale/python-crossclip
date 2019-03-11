
# crossclip -- cross platform clipboard API
# Copyright (C) 2019  Charlie Sale

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# clipboard.py -- frontend clipboard class

import sys
from . import platform_backend, backends
import PIL

class Clipboard:
    """ Frontend to various clipboard backends

    This class is a frontend for the various backends. It automatically
    determines which backend should be used based on whatever the platform
    is.
    """
    backend_type = None
    backend = None
    image_converter = None

    def __init__(self, clip_backend=platform_backend):
        """
        Creates a new clipboard that interfaces one of the platform-specific
        backends. The backend is implicitly deduced, but a specific backend
        can be choosen instead.
        :param clip_backend: Which backend to use. Defaults to implicitly-selected backend
        :raises RuntimeError: If clip_backend is invalid
        """
        # Choose the backend to use
        if clip_backend not in backends:
            raise RuntimeError('Invalid backend selected')

        self.backend = backends[clip_backend]
        self.backend_type = clip_backend

        # Based off of backend, get the native image type (e.g QImage)
        self.image_converter = self.backend.image_converter

    def get_text(self) -> str:
        """
        Gets text from the clipboard.
        :returns str: Text from clipboard or None if no text is available
        """
        return self.backend.get_text()

    def get_image(self, native=False):
        """
        Gets an image from the clipboard.
        :param native: If true, then the returned image will be of type `self.image_converter.image_type`.
                        If False, then object will be of type `PIL.Image`.
        :returns `PIL.Image` or `self.image_converter.image_type`: Initialized image object or None if no image is available
        """
        if native is True:
            return self.backend.get_image(format=self.image_converter.image_str)
        else:
            return self.backend.get_image()

    def set_text(self, text: str):
        """
        Places text on the clipboard.
        :param text: Text to add
        """
        self.backend.set_text(text)

    def set_image(self, image):
        """
        Sets an image on the clipboard. Image can either be of type `PIL.Image` or
        `self.image_converter.image_str`.
        :param image: image to be placed.
        :raises RuntimeError: If image is neither of type `PIL.Image` nor `self.image_converter.image_type`
        """
        if isinstance(image, self.image_converter.image_type):
            self.backend.set_image(image, format=self.image_converter.image_str)
        elif isinstance(image, PIL.Image.Image):
            self.backend.set_image(image)
        else:
            raise RuntimeError('Image must be of type `PIL.Image` or `self.image_converter.image_str`')
