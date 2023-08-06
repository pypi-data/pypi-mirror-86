
from subprocess import check_call, Popen, PIPE
from functools import partial

from .. import defaults
from .shutil import which

def resolve_path(f):
    def call(cmd, **kwargs):
        ex = cmd[0]
        ex = which(ex) or ex
        return f([ex] + list(cmd[1:]), **kwargs)  # list-conversion is required in case `cmd` is a tuple
    return call

if defaults.WINDOWS:
    check_call = partial(resolve_path(check_call), shell=True)
    Popen = resolve_path(Popen)