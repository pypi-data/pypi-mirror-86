__version__ = '0.1.2.7'

from .rosclients import MobileClient, CameraListener
from . import area_globalization
from . import occupancygrid_utils

__all__ = ['MobileClient', 'CameraListener', 'area_globalization', 'occupancygrid_utils']

## EX: 
# import rosmobilelib
# import rosmobilelib.rostools 