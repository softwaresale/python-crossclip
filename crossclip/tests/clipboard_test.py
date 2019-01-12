
import unittest
import sys
from ..backends import (
    BACKEND_TO_USE,
    GtkBackend,
    QtBackend,
    WindowsBackend,
)
from ..clipboard import Clipboard
from PIL import Image as PilImage
from PIL import ImageChops as PilImageChops
import numpy

def generate_random_image(image_format='RGB'):
    imarray = numpy.random.rand(100, 100, 3) * 255
    # TODO: for now, clipboard does not support RGBA. This will need some
    # work
    test_image = PilImage.fromarray(imarray.astype('uint8')).convert(image_format)
    return test_image

def eval_images(image1, image2):
    """ Function to verify that two images are the same
    """
    return PilImageChops.difference(image1, image2).getbbox() is None

@unittest.skipUnless(BACKEND_TO_USE == 'gtk', 'Not using GTK backend')
class GtkTestCase(unittest.TestCase):

    def setUp(self):
        # Create clipboard. Make sure that it is valid
        self.clipboard = Clipboard()
        self.assertTrue(self.clipboard is not None)
        self.assertTrue(self.clipboard.backend_type is GtkBackend)
        self.assertTrue(self.clipboard.image_str == 'gdk')

    def test_text(self):
        # Test putting text onto the clipboard
        msg = 'Hello World'
        self.clipboard.set_text(msg)

        # Test getting above text
        text = self.clipboard.get_text()
        self.assertTrue(text is not None)
        self.assertTrue(text == msg)

    def test_image(self):
        # Open the test image
        test_image = generate_random_image()

        # Put image on the clipboard
        self.clipboard.set_image(test_image)

        # Get image from clipboard, verify equality
        new_image = self.clipboard.get_image()
        self.assertTrue(
            eval_images(test_image, new_image)
        )

    def test_image_loss(self):
        # Create test iamge with RGBA
        test_image = generate_random_image('RGBA')

        # Put image on clipboard
        self.clipboard.set_image(test_image)

        # Test image equality
        new_image = self.clipboard.get_image()
        self.assertFalse(
            eval_images(test_image, new_image.convert('RGBA'))
        )

@unittest.skipUnless(BACKEND_TO_USE == 'qt', 'Not using Qt backend')
class QtTestCase(unittest.TestCase):

    def setUp(self):
        # Create clipboard. Make sure that it is valid
        self.clipboard = Clipboard()
        self.assertTrue(self.clipboard is not None)
        self.assertTrue(self.clipboard.backend_type is QtBackend)
        self.assertTrue(self.clipboard.image_str == 'qt')

    def test_text(self):
        # Test putting text onto the clipboard
        msg = 'Hello World'
        self.clipboard.set_text(msg)

        # Test getting above text
        text = self.clipboard.get_text()
        self.assertTrue(text is not None)
        self.assertTrue(text == msg)

    def test_image(self):
        # Open the test image
        test_image = generate_random_image()

        # Put image on the clipboard
        self.clipboard.set_image(test_image)

        # Get image from clipboard, verify equality
        new_image = self.clipboard.get_image()
        self.assertTrue(
            eval_images(test_image, new_image)
        )

@unittest.skipUnless(BACKEND_TO_USE == 'win32', 'Not using windows backend')
class WinTestCase(unittest.TestCase):

    def setUp(self):
        # Create clipboard. Make sure that it is valid
        self.clipboard = Clipboard()
        self.assertTrue(self.clipboard is not None)
        self.assertTrue(self.clipboard.backend_type is WindowsBackend)
        self.assertTrue(self.clipboard.image_str == 'pil')

    def test_text(self):
        # Test putting text onto the clipboard
        msg = 'Hello World'
        self.clipboard.set_text(msg)

        # Test getting above text
        text = self.clipboard.get_text()
        self.assertTrue(text is not None)
        self.assertTrue(text == msg)

    def test_image(self):
        # Open the test image
        test_image = generate_random_image()

        # Put image on the clipboard
        self.clipboard.set_image(test_image)

        # Get image from clipboard, verify equality
        new_image = self.clipboard.get_image()
        self.assertTrue(
            eval_images(test_image, new_image)
        )
