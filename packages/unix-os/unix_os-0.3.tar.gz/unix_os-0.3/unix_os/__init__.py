from os import *

if name == 'nt':
    # shadowing os with local definitions
    from .path import *
    from . import path

    sep = '/'

    from .unix_glob import *

else:

    from glob import *
