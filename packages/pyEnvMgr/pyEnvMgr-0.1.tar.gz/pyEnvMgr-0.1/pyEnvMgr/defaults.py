from pathlib import Path
from . import tools
import os
import sys


IS_PY2 = sys.version_info[0] == 2
WINDOWS = sys.platform == 'win32'
ENV_BIN_DIR = 'bin' if not WINDOWS else 'Scripts'


if WINDOWS:
    DEFAULT_HOME = '~/.virtualenvs'
else:
    DEFAULT_HOME = os.path.join(
        os.environ.get('XDG_DATA_HOME', '~/.local/share'), 'virtualenvs')

WORKON_HOME = tools.expandpath(
    os.environ.get('WORKON_HOME', DEFAULT_HOME)
)

SPECIALS_WINDOWS_SHELLS = (
    'Cmder',
    'bash',
    'elvish',
    'powershell',
    'klingon',
    'cmd',
)

ENV_DIR_VAR = "PYENVMGR_DIR"
DEFAULT_ENV_DIR_NAME = ".pyenvmgr"
DEFAULT_ENV_DIR = Path.home() / DEFAULT_ENV_DIR_NAME

def get_env_dir():
    directory = tools.dir_from_env(ENV_DIR_VAR) or DEFAULT_ENV_DIR
    if not directory.exists():
        directory.mkdir()
    return directory


ENV_DIR = get_env_dir()