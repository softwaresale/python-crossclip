
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

# frontend.py -- frontend class

import sys
from .backends import *

class Clipboard:
    """ Frontend to various clipboard backends

    This class is a frontend for the various backends. It automatically
    determines which backend should be used based on whatever the platform
    is.
    """
    backend_type = None
    backend = None
    image_type = None
    image_str = None

    def __init__(self):
        """ Constructs a new object and chooses the backend

        The backend is choosen automatically based on the host platform.
        """
        # Choose the backend based off of BACKEND_TO_USE
        if BACKEND_TO_USE == 'gtk':
            self.backend = GtkBackend()
            self.backend_type = GtkBackend
        elif BACKEND_TO_USE == 'qt':
            self.backend = QtBackend()
            self.backend_type = GtkBackend
        elif BACKEND_TO_USE == 'win32':
            pass
        elif BACKEND_TO_USE == 'darwin':
            pass
        else:
            raise RuntimeError('Invalid backend')

        # Based off of backend, get the native image type (e.g QImage)
        self.image_str = self.backend.get_native_image_str()
        self.image_type = self.backend.get_native_image_type()

    def get_text(self):
        return self.backend.get_text()

    def get_image(self, native=False):
        if native is True:
            return self.backend.get_image(format=self.image_str)
        else:
            return self.backend.get_image()

    def set_text(self, text):
        self.backend.set_text(text)

    def set_image(self, image, native=False):
        if native is True:
            self.backend.set_image(image, format=self.image_str)
        else:
            self.backend.set_image(image)