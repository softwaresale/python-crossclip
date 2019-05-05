
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
        cross_cb = Clipboard(instance=clipboard)
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
        cross_cb = Clipboard(instance=clipboard)
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
        cross_cb = Clipboard(instance=clipboard)
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


class AbstractClipboardListener(ABC):

    handler = None

    @staticmethod
    def run_listener(listener, handler=None):
        """ Runs an instantiated listener.

        Runs a clipboard listener as a task.
        :param listener: Instantiated listener instance
        :type listener: ClipboardListener
        :param handler_type: Type of event handler. Note: NOT AN INSTANCE
        :type handler_type: subclass of AbstractEvent
        :return: Created coroutine task
        :rtype: asyncio.Task
        """
        return asyncio.create_task(listener.start(handler()))

    def __init__(self, clipboard=None):
        """ Create a new listener

        Create a new clipboard listener. You can wrap it around
        a new or existing clipboard.
        :param clipboard: Clipboard instance (default None)
        :type clipboard: crossclip.clipboard.Clipboard
        """
        self._handler = None
        if clipboard is None:
            self.clipboard = Clipboard()
        else:
            self.clipboard = clipboard

    @abstractmethod
    async def start(self, handler=None):
        pass
