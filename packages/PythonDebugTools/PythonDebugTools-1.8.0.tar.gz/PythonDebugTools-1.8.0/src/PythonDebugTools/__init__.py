import sys

from .__version__ import *
from .colors import *
from .console import *
from .converters import *
from .decorators import *




def get_size(obj, seen: set = set()):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None: seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size



__name__ = 'PythonDebugTools'
__author__ = "Tyler Stegmaier"
__email__ = "tyler.stegmaier.510@gmail.com"
__copyright__ = "Copyright 2020"
__credits__ = [
        "Copyright (c) 2020 Tyler Stegmaier",
        ]
__license__ = "GPL 3.0"
__version__ = version
__maintainer__ = __author__
__maintainer_email__ = __email__

# How mature is this project? Common values are
#   3 - Alpha
#   4 - Beta
#   5 - Production/Stable
__status__ = 'Development Status :: 4 - Beta'

__url__ = fr'https://github.com/Jakar510/{__name__}'
# download_url=f'https://github.com/Jakar510/PyDebug/TkinterExtensions/releases/tag/{version}'
__classifiers__ = [
        __status__,

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: Free To Use But Restricted',

        # Support platforms
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
        ]

__short_description__ = 'A set of helpers for debugging Python 3.x.'
