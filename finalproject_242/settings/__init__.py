import os

from settings_base import *

cwd = os.getcwd()
if cwd == '/app':
    from settings_production_http import *
else:
    from settings_local import *
