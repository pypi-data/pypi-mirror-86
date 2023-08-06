import os
import sys
from pathlib import Path
from . import defaults
from .tools import expandpath, temp_environ
from .compatility import (
    check_call,
    NamedTemporaryFile,
    to_unicode,
    detect_shell,
)
from subprocess import CalledProcessError
from functools import partial


err = partial(print, file=sys.stderr)


def supported_shell():
    shell = Path(os.environ.get('SHELL', '')).stem
    if shell in ('bash', 'zsh', 'fish'):
        return shell

def unsetenv(key):
    if key in os.environ:
        del os.environ[key]


def compute_path(env):
    envdir = defaults.ENV_DIR / env
    return os.pathsep.join([
        str(envdir / defaults.ENV_BIN_DIR),
        os.environ['PATH'],
    ])


def run_in(env, command, *args, **kwargs):
    """Run a command in the given virtual environment.
    Pass additional keyword arguments to ``subprocess.check_call()``."""
    # we don't strictly need to restore the environment, since it runs in
    # its own process, but it feels like the right thing to do
    with temp_environ():
        os.environ['VIRTUAL_ENV'] = str(defaults.ENV_DIR / env)
        os.environ['PATH'] = compute_path(env)

        unsetenv('PYTHONHOME')
        unsetenv('__PYVENV_LAUNCHER__')

        try:
            return check_call([command] + list(args), **kwargs)
            # need to have shell=True on defaults.WINDOWS, otherwise the PYTHONPATH
            # won't inherit the PATH
        except OSError as e:
            if e.errno == 2:
                err('Unable to find', command)
                return e.errno
            else:
                raise


def _fork_shell(env, shellcmd, cwd):
    or_ctrld = '' if defaults.WINDOWS else "or 'Ctrl+D' "
    err("Launching subshell in virtual environment. Type 'exit' ", or_ctrld,
        "to return.", sep='')
    if 'VIRTUAL_ENV' in os.environ:
        err("Be aware that this environment will be nested on top "
            "of '%s'" % Path(os.environ['VIRTUAL_ENV']).name)
    return run_in(env, *shellcmd, cwd=cwd)


def fork_bash(env, cwd):
    # bash is a special little snowflake, and prevent_path_errors cannot work there
    # https://github.com/berdario/pew/issues/58#issuecomment-102182346
    bashrcpath = expandpath('~/.bashrc')
    if bashrcpath.exists():
        with NamedTemporaryFile('w+') as rcfile:
            with bashrcpath.open() as bashrc:
                rcfile.write(bashrc.read())
            rcfile.write('\nexport PATH="' + to_unicode(compute_path(env)) + '"')
            rcfile.flush()
            return _fork_shell(env, ['bash', '--rcfile', rcfile.name], cwd)
    else:
        return _fork_shell(env, ['bash'], cwd)


def fork_cmder(env, cwd):
    shell_cmd = ['cmd']
    cmderrc_path = r'%CMDER_ROOT%\vendor\init.bat'
    if expandpath(cmderrc_path).exists():
        shell_cmd += ['/k', cmderrc_path]
    if cwd:
        os.environ['CMDER_START'] = cwd
    return _fork_shell(env, shell_cmd, cwd)

def is_shell_valide(env, shell):
    return True
    # TODO: Fix code

    shell_name = Path(shell).stem
    if shell_name not in defaults.SPECIALS_WINDOWS_SHELLS:
        # On defaults.WINDOWS the PATH is usually set with System Utility
        # so we won't worry about trying to check mistakes there
        shell_check = (sys.executable + ' -c "from pew.pew import '
                       'prevent_path_errors; prevent_path_errors()"')
        try:
            run_in(env, shell, '-c', shell_check)
        except CalledProcessError:
            return False
    return True

def fork_shell(env, shell, cwd):
    shell_name = Path(shell).stem
    if shell_name == 'bash':
        return fork_bash(env, cwd)
    elif shell_name == 'Cmder':
        return fork_cmder(env, cwd)
    else:
        return _fork_shell(env, [shell], cwd)

def shell(env, cwd=None):
    env = str(env)
    shell = detect_shell()
    # Check if the shell is allowed
    if not is_shell_valide(env, shell):
        return
    return fork_shell(env, shell, cwd)