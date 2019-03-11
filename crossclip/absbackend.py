
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

# backends.py -- backend classes

import sys
import os
from abc import ABC, abstractmethod, abstractstaticmethod, abstractproperty

class AbstractBackend(object):
    """ Interface for all clipboard backends

    This class is an interface for all clipboard backends to
    be registered into.
    """
    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_image(self, format='Pil'):
        pass

    @abstractmethod
    def set_text(self, text):
        pass

    @abstractmethod
    def set_image(self, img, format='pil'):
        pass

class AbstractImageConverter:
    
    @abstractproperty
    def image_type(self):
        pass

    @abstractproperty
    def image_str(self):
        pass

    @abstractmethod
    def to_pillow(native_image):
        pass

    @abstractmethod
    def from_pillow(pil):
        pass