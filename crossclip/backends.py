
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

# BaseBackend.py -- base class for all backends

import sys

# Do some cross-platform importing. This module does not support
# cygwin. 
# On linux, the system first looks for Gtk via PyGObject.
# If that is not found, then it tries to get Qt. If neither are
# found, then an error is thrown. Ill try to support more formats
# in the future, but as of now, I am operating under the premise
# that everyone that would be using this on linux is using either
# a GTK or a Qt based desktop.
# On OSX, I use PyObjC to access the system clipboard. I will consider
# adding fallback support to use pb(copy|paste) as a backup.
# On windows, use the win32clipboard module. If that's not found, then
# no dice.
if sys.platform == 'linux':
    try:
        # Try to import GTK first.
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        from gi.repository import Gdk
        from gi.repository import GdkPixbuf
        from gi.repository import GLib
    except ModuleNotFoundError:
        # if Gtk is not found, then try to import pyqt
        try:
            from PyQt5.Qt import QApplication, QClipboard
            import PyQt5
        except ModuleNotFoundError:
            raise RuntimeError("You have neither Qt or GTK installed. Please install either PyGobject or PyQt5")
elif sys.platform == 'darwin':
    try:
        # Try getting PyObjC
        from AppKit import NSPasteboard, NSStringPboardType
    except ModuleNotFoundError:
        raise RuntimeError("You need PyObjC if you are running on mac")
elif sys.platform == 'win32':
    try:
        import win32clipboard
    except ModuleNotFoundError:
        raise RuntimeError("You need pywin32 to run on windows")
else:
    raise RuntimeError('Your platform is not supported')

from PIL import Image as PilImage

class BaseBackend(object):
    """ Interface for all clipboard backends

    This class is an interface for all clipboard backends to
    be registered into.
    """
    def get_text(self):   
        """ Synchronously get text

        Preform a blocking call to get text from the clipboard

        Returns
        -------
        str or None
            String if text is ever gotten, or None if there is no text
        """
        raise NotImplementedError

    def get_image(self, format='Pil'):
        """ Synchronously get image

        Preform a blocking call to get an image from the clipboard

        Params
        ----------
        format : str (optional)
            Format of the image. Default is 'Pil', which refers to
            PIL.Image, but implementation is left to each function

        Returns
        -------
        PIL.Image or None
            Image from clipboard, or None if not available
        """
        raise NotImplementedError

    def set_text(self, text):
        """ Synchronously sets text

        Preform a blocking call to set text on the clipboard

        Params
        ----------
        text : str
            Text to add to clipboard
        """
        raise NotImplementedError

    def set_image(self, img):
        """ Synchronously sets image

        Preform a blocking call to set image on the clipboard

        Params
        ----------
        image : PIL.Image
            Image to add to clipboard
        """
        raise NotImplementedError

class GtkBackend(BaseBackend):
    """ Gtk Clipboard backend

    This clipboard backends the Gtk.Clipboard class. It inherits from it and
    the base backend class. This way, it has all of the Gtk's properties, but
    it can operate through the BaseBackend interface.
    """

    @staticmethod
    def pixbuf_to_image(pixbuf):
        """ Converts a GdkPixbuf.Pixbuf to PIL.Image

        This converts Gdk pixbuf to Pil Image. PIL Images are used by the front-end,
        but the user may also want to access a raw GdkPixbuf.
        """
        data = pixbuf.get_pixels()
        w = pixbuf.props.width
        h = pixbuf.props.height
        stride = pixbuf.props.rowstride
        mode = "RGB"
        if pixbuf.props.has_alpha == True:
            mode = "RGBA"
        return PilImage.frombytes(mode, (w, h), data, "raw", mode, stride)

    @staticmethod
    def image_to_pixbuf(image):
        """ Convert PIL.Image to GdkPixbuf.Pixbuf

        This converts a PIL Image to Gdk Pixbuf
        """
        data = image.tobytes()
        w, h = image.size
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3)

    def __init__(self, display=None):
        """ Constructs a new object

        Creates a new clipboard from the given display, which is optional

        Params
        ------
        display : Gdk.Display, optional
            Display to get clipboard from
        """
        if display is None:
            display = Gdk.Display.get_default()
        BaseBackend.__init__(self)
        self.clipboard = Gtk.Clipboard.get_default(display)

    def get_text(self):
        """ Synchronously get text

        Preform a blocking call to get text from the clipboard

        Returns
        -------
        str or None
            String if text is ever gotten, or None if there is no text
        """
        text = self.clipboard.wait_for_text()
        return text

    def get_image(self, format='pil'):
        """ Synchronously get image

        Preform a blocking call to get an image from the clipboard

        Params
        ----------
        format : str (optional)
            Format of the image. Default is 'pil', which refers to
            PIL.Image, 'gdk', which refers to a GdkPixbuf.Pixbuf, or
            'raw', which refers to raw data.

        Returns
        -------
        PIL.Image, GdkPixbuf.Pixbuf, Glib.Bytes, or None
            Image from clipboard, or None if not available or bad format
        """
        pixbuf = self.clipboard.wait_for_image()
        if format == 'gdk':
            return pixbuf
        elif format == 'raw':
            return pixbuf.read_pixel_bytes()
        elif format == 'pil':
            return GtkBackend.pixbuf_to_image(pixbuf)
        else:
            raise RuntimeWarning('Image format is not supported')
            return None
            
    def set_text(self, text, num=-1):
        """ Synchronously sets text

        Preform a blocking call to set text on the clipboard.

        Params
        ----------
        text : str
            Text to add to clipboard
        num : int, optional
            Length of text to copy to clipboard
        """
        # Assuming that all text is to be copied over
        self.clipboard.set_text(self, text, num)
    
    def set_image(self, image, format='pil'):
        """ Synchronously sets image

        Preform a blocking call to set image on the clipboard

        Params
        ----------
        image : PIL.Image, GdkPixbuf.Pixbuf
            Image to add to clipboard

        format : str
            Format of image. Can be 'pil' for PIL.Image, or 'gdk'
            for GdkPixbuf.Pixbuf
        """
        if format == 'gdk':
            self.clipboard.set_image(image)
        elif format == 'pil':
            pixbuf = GtkBackend.image_to_pixbuf(image)
            self.clipboard.set_image(pixbuf)
        else:
            raise RuntimeWarning('Invalid image format')
            return None

