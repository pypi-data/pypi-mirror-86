import glob as _glob

with open(_glob.__file__, 'r') as f:
    tmp = f.read().replace('import os', 'import unix_os as os')

exec(tmp)
