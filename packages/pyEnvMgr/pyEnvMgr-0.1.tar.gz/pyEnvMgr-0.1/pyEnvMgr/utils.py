import os
import sys
from collections import namedtuple
from . import defaults
from .compatility import (
    which,
    ENCODING,
    Popen,
    PIPE
)

def check_path():
    parent = os.path.dirname
    return parent(parent(which('python'))) == os.environ['VIRTUAL_ENV']

Result = namedtuple('Result', 'returncode out err')


# TODO: it's better to fail early, and thus I'd need to check the exit code, but it'll
# need a refactoring of a couple of tests
def invoke(*args, **kwargs):
    inp = kwargs.pop('inp', '').encode(ENCODING)
    popen = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
    out, err = [o.strip().decode(ENCODING) for o in popen.communicate(inp)]
    return Result(popen.returncode, out, err)


# invoke_pew = partial(invoke, 'pew')



def own(path):
    # Copy to have lazy check
    if sys.platform == 'win32':
        # Even if run by an administrator, the permissions will be set
        # correctly on defaults.WINDOWS, no need to check
        return True
    while not path.exists():
        path = path.parent
    return path.stat().st_uid == os.getuid()

