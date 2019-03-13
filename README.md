# Crossclip
A cross platform clipboard API for python.

# Current State of the Package
Backends are written but untested. Package needs a better test
suite.

## Overview

### About
Crossclip provides a standard python API for interacting with the system
clipboard. As of now, Crossclip supports MacOS, Windows, and GNU/Linux desktop
environments using Gtk and Qt environments. More environments can be added due
to the modular design.

### Dependencies

#### All systems
* Pillow (5.4.0)

#### Linux
* Gtk users: PyGObject
* Qt users: PySide2

#### Windows
* pywin32

#### Mac
* pyobjc

### Installation
This package is hosted on PyPI. Install via:

`$ pip install crossclip`

### Usage
Here is an example program:
```
# Import the clipboard frontend class and Pillow Image package
from crossclip.clipboard import Clipboard
from PIL import Image

# Create a new clipboard instance
cb = Clipboard()

# Get text from the clipboard
mytext = cb.get_text()

# Get an image from the clipboard
myimg = cb.get_image() # myimg is a PIL.Image class

# Put text onto the clipboard
my_message = 'Hello World'
cb.set_text(my_message)

# Put an image onto the clipboard
cb.set_image(my_pil_image_instance)

# Access the backend instance
backend_text = cb.backend.get_text()
```

It's as easy as that. The frontend wraps all of the backend specifics and
provides a simple, uniform interface.

## Implementation Details
This library uses a collection of backends to provide clipboard functionality
for a specific system or clipboard. For example, there is a clipboard backend
for the Windows system clipboard and the Gtk+ clipboard. Each backend inherits
from an abstract base class that provides a set of common abstract methods that
each backend must implement.

Each of these backends are used in the frontend class, `clipboard.Clipboard`.
The `Clipboard` class determines the backend to use based on the system platform
determined by the `sys.platform` value. The Clipboard class carries an instance
of the backend and uses its functions to provide clipboard functionality.

With a design like this, the library is extensible. New backends can be added
and removed.

## Contributing
See CONTRIBUTING.md

## License
This package is licensed under the GPLv3.
