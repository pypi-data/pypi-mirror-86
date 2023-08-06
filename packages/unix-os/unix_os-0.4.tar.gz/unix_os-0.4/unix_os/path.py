import os as _os
from os.path import *
import re as _re


def join(a, *p):
    return '/'.join([a] + list(p))


join.__doc__ = _os.path.join.__doc__


for _item in ['normpath', 'abspath']:
    _str = f'''
def {_item}(path):
    return _os.path.{_item}(path).replace('\\\\', '/')

{_item}.__doc__ = _os.path.{_item}.__doc__
'''
    exec(_str)


def nt_sanitize(path):
    '''
    replace windows `\` with unix `/`

    :param path: path string

    :return: sanitized path
    '''
    return path.replace('\\\\', '/').replace('\\', '/')


def process_cygdrive(path):
    if _os.path.exists('/cygdrive'):
        drive = _re.match('^([A-Z]):/.*', path)
        if drive:
            return f"/cygdrive/{drive.groups()[0].lower()}/{_re.sub('^[A-Z]:/', '', path)}"
        else:
            return path
