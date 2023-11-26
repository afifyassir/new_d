import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.config.core import PACKAGE_ROOT, config  # noqa: E402

logging.getLogger(config.app_config.package_name).addHandler(logging.NullHandler())

with open(os.path.join(PACKAGE_ROOT, "VERSION")) as version_file:
    __version__ = version_file.read().strip()

