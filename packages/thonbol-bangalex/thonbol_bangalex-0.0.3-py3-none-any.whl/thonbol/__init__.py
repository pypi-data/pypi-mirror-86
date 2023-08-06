from __future__ import absolute_import

from ._people import People
from ._version import __version__

import logging

logger = logging.getLogger("thonbol")
if logger.level is logging.NOTSET:
    logger.setLevel(logging.CRITICAL)
del logger
__all__ = [
        "People",
        "__version__"
]
