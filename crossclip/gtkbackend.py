
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

# gtkbackend.py -- Defines GTK backend

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from PIL import Image as PilImage
from io import BytesIO

from .absbackend import AbstractBackend, AbstractImageConverter

class GtkImageConverter(AbstractImageConverter):

    @property
    def image_type(self):
        """
        Returns the type of image that this converter uses.
        :returns: GdkPixbuf.Pixbuf type (not object!)
        """
        return GdkPixbuf.Pixbuf

    @property
    def image_str(self):
        """
        Returns a string representation of what the object is.
        :returns str: 'gdk-pixbuf'
        """
        return 'gdk-pixbuf'

    def to_pillow(self, pixbuf):
        """
        Converts and image of `self.image_type` to a `PIL.Image`.
        :param pixbuf: GdkPixbuf.Pixbuf image
        :returns PIL.Image: Converted Pillow Image
        """
        data = pixbuf.get_pixels()
        w = pixbuf.props.width
        h = pixbuf.props.height
        stride = pixbuf.props.rowstride
        mode = "RGB"
        if pixbuf.props.has_alpha == True:
            mode = "RGBA"
        return PilImage.frombytes(mode, (w, h), data, "raw", mode, stride)

    def from_pillow(self, image):
        """
        Converts a `PIL.Image` to a `GdkPixbuf.Pixbuf`.
        :param image: `PIL.Image` to be convered
        :returns GdkPixbuf.Pixbuf: Converted pixbuf
        """
        # data = image.tobytes()
        # w, h = image.size
        # data = GLib.Bytes.new(data)
        # pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3)
        # return pix
        ibuf = BytesIO()
        image.save(ibuf, format='png')
        loader = GdkPixbuf.PixbufLoader.new_with_mime_type('image/png')
        status = loader.write(ibuf.getvalue())
        if status:
            pixbuf = loader.get_pixbuf()
            loader.close()
            return pixbuf
        else:
            return None

class GtkBackend(AbstractBackend):
    """ Gtk Clipboard backend

    This clipboard backends the Gtk.Clipboard class. It inherits from it and
    the base backend class. This way, it has all of the Gtk's properties, but
    it can operate through the BaseBackend interface.
    """

    image_converter = GtkImageConverter()

    def __init__(self, display=None):
        if display is None:
            display = Gdk.Display.get_default()
        super().__init__()
        self.clipboard = Gtk.Clipboard.get_default(display)

    def get_text(self) -> str:
        """
        Synchronously gets text from clipboard.
        :return str: Text from clipboard
        """
        text = self.clipboard.wait_for_text()
        return text

    def get_image(self, format='pil'):
        """
        Synchronously gets image from clipboard. The image is either
        a pillow image, or a GdkPixbuf.Pixbuf.
        :param format: Format of image. 'pil' for pillow, 'gdk-pixbuf' for gdk pixbuf (default: 'pil')
        :returns PIL.Image or GdkPixbuf.Pixbuf: Image in chosen format
        :raises RuntimeWarning: If format is invalid format
        """
        pixbuf = self.clipboard.wait_for_image()
        if pixbuf is None:
            return None
        if format == self.image_converter.image_str:
            return pixbuf
        elif format == 'pil':
            return self.image_converter.to_pillow(pixbuf)
        else:
            raise RuntimeWarning('Image format is not supported')
            return None
            
    def set_text(self, text: str, num=-1):
        """
        Synchronously sets text to clipboard
        :param text: text to set to clipboard
        :param num: length of text to set. If -1, all text is copied (default: -1)
        """
        # Assuming that all text is to be copied over
        self.clipboard.set_text(text, num)
    
    def set_image(self, image, format='pil'):
        """
        Synchronously sets image to clipboard.
        :param image: Some image object
        :param format: format of image
        :raises RuntimeWarning: If format is invalid
        """
        if format == self.image_converter.image_str:
            self.clipboard.set_image(image)
        elif format == 'pil':
            pixbuf = self.image_converter.from_pillow(image)
            self.clipboard.set_image(pixbuf)
        else:
            raise RuntimeWarning('Invalid image format')
            return None
