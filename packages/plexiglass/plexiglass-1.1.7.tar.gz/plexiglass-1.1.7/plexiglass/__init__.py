import os
from . import adversarial
from . import detectors
with open(os.path.join(os.path.dirname(__file__), 'version')) as f:
    __version__ = f.read().strip()