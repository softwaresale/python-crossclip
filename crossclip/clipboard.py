
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
from .absbackend import AbstractBackend, AbstractClipboardListener, AbstractImageConverter
import PIL

class Clipboard:
    """ Frontend to various clipboard backends

    This class is a frontend for the various backends. It automatically
    determines which backend should be used based on whatever the platform
    is.
    """

    @property
    def backend_type(self):
        if issubclass(self._backend_type, AbstractBackend):
            return self._backend_type
        else:
            return None

    @backend_type.setter
    def backend_type(self, new_type):
        if issubclass(new_type, AbstractBackend):
            self._backend_type = new_type
        else:
            return None

    @property
    def backend(self):
        if isinstance(self._backend, AbstractBackend):
            return self._backend
        else:
            return None

    @backend.setter
    def backend(self, new_backend):
        if isinstance(new_backend, AbstractBackend):
            self._backend = new_backend
        else:
            return None

    @property
    def listener_type(self):
        if issubclass(self._listener_type, AbstractClipboardListener):
            return self._listener_type
        else:
            return None

    @listener_type.setter
    def listener_type(self, new_type):
        if issubclass(new_type, AbstractClipboardListener):
            self._listener_type = new_type
        else:
            return None

    @property
    def listener(self):
        if isinstance(self._listener, AbstractBackend):
            return self._listener
        else:
            return None

    @listener.setter
    def listener(self, new_listener):
        if isinstance(new_listener, AbstractClipboardListener):
            self._listener = new_listener
        else:
            return None

    image_converter = None
    """ Image converter instance
    """

    @staticmethod
    def from_clipboard_instance(raw_instance):
        if isinstance(raw_instance, backends['gtk']):
            return Clipboard(backends['gtk'], raw_instance)
        elif isinstance(raw_instance, backends['qt']):
            return Clipboard(backends['qt'], raw_instance)
        else:
            return None

    def __init__(self, clip_backend_type=backends[platform_backend], instance=None):
        """
        Creates a new clipboard that interfaces one of the platform-specific
        backends. The backend is implicitly deduced, but a specific backend
        can be choosen instead.

        :param clip_backend: Which backend to use. Defaults to implicitly-selected backend
        :type clip_backend: instance of `AbstractBackend`
        :raises RuntimeError: If clip_backend is invalid
        """
        # Choose the backend to use
        #if clip_backend not in backends:
        #    raise RuntimeError('Invalid backend selected')

        # Verify validity of backend type
        if not issubclass(clip_backend_type, AbstractBackend):
            raise RuntimeError("Clipboard backend is of invalid type")

        self._backend = clip_backend_type(instance=instance)
        self._backend_type = clip_backend_type

        # Based off of backend, get the native image type (e.g QImage)
        self._image_converter = self.backend.image_converter

        # Set the listener type
        self._listener_type = self.backend.listener_type

        # Set the listener instance to None
        self._listener = None

    def __del__(self):
        # Clean up listeners if not already done
        self.stop_listener()

    def get_text(self):
        """
        Gets text from the clipboard.

        :returns: Text from clipboard or None if no text is available
        :rtype: str
        """
        return self.backend.get_text()

    def get_image(self, form='pil', converter=None):
        """
        Gets an image from the clipboard.

        :param native: If true, then the returned image will be of type `self.image_converter.image_type`.
                        If False, then object will be of type `PIL.Image`.
        :type native: boolean
        :returns: Initialized image object or None if no image is available
        :rtype: `PIL.Image` or `self.image_converter.image_type`
        """
        return self.backend.get_image(form, converter)

    def set_text(self, text: str):
        """
        Places text on the clipboard.

        :param text: Text to add
        :type text: str
        """
        self.backend.set_text(text)

    def set_image(self, image):
        """
        Sets an image on the clipboard. Image can either be of type `PIL.Image` or
        `self.image_converter.image_type`.

        :param image: image to be placed.
        :type image: instance of `PIL.Image` or `self.image_converter.image_type`
        :raises RuntimeError: If image is neither of type `PIL.Image` nor `self.image_converter.image_type`
        """
        self.backend.set_image(image)

    def start_listener(self, event_handler):
        """ Start a clipboard event monitor

        This method starts a new clipboard event listener. Once this is started, it will
        monitor any clipboard events and handle them with the event_handler.
        :param event_handler: Event to handle
        :type event_handler: AbstractEvent
        """
        listener_instance = self.listener_type(self)
        self.listener = AbstractClipboardListener.run_listener(listener_instance, event_handler)

    def stop_listener(self):
        """ Stops the event monitor

        If it hasn't already been stopped. This method stops the event
        monitor.
        """
        if not self.listener.cancelled() and not self.listener.done():
            self.listener.cancel()
