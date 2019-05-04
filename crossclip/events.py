
import abc
from .clipboard import Clipboard

class AbstractEvent(abc.ABC):
    """
    Creates a generic clipboard event. Any subsequent clipboard
    event is created by deriving this and overriding the handle
    method.
    """
    def __call__(self, clipboard, *args):
        """
        Overridding this method makes the object callable. All
        this method does is wrap the handle method. It can also
        pass additional information into the handle method.
        :param clipboard: raw clipboard instance
        :type clipboard: clipboard.raw_clipboard_type
        """
        cross_cb = Clipboard.from_clipboard_instance(clipboard)
        self.handle(cross_cb, *args)

    @abc.abstractmethod
    def handle(self, clipboard, *args):
        """ Method called on event

        This method is defined by the user to handle an event.
        :param clipboard: Clipboard instance that is source of event
        :type clipboard: crossclip.clipboard.Clipboard
        """
        pass

class OnTextChangeEvent(AbstractEvent):
    """ Event to monitor changes in text

    This event is a simple subclass of AbstractEvent which monitors
    changes in text.
    """

    def __call__(self, clipboard, *args):
        cross_cb = Clipboard.from_clipboard_instance(clipboard)
        text = str()
        if cross_cb.backend.wait_text_is_available():
            text = cross_cb.get_text()
            self.handle(cross_cb, text, *args)
        else:
            # There is no text to handle
            return None

    @abc.abstractmethod
    def handle(self, clipboard, text, *args):
        """ Method called on event

        This method is defined by the user to handle an event.
        :param clipboard: Clipboard instance that is source of event
        :type clipboard: crossclip.clipboard.Clipboard
        :param text: new text
        :type text: str
        """
        pass

class OnImageChangeEvent(AbstractEvent):

    def __call__(self, clipboard, *args):
        cross_cb = Clipboard.from_clipboard_instance(clipboard)
        if clipboard.wait_is_image_available():
            img = cross_cb.get_image()
            self.handle(cross_cb, img, *args)
        else:
            return None

    @abc.abstractmethod
    def handle(self, clipboard, img, *args):
        """ Method called on image event

        This method is defined by the user to handle an image changed event.
        :param clipboard: Clipboard instance that is source of event
        :type clipboard: crossclip.clipboard.Clipboard
        :param img: New image
        :type img: clipboard.image_type
        """
        pass

