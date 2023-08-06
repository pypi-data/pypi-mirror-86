import os
import sys
from .. import defaults

if not defaults.WINDOWS:
    try:
        # Try importing these packages if avaiable
        from pythonz.commands.install import InstallCommand
        from pythonz.commands.uninstall import UninstallCommand
        from pythonz.installer.pythoninstaller import PythonInstaller, AlreadyInstalledError
        from pythonz.commands.list import ListCommand
        from pythonz.define import PATH_PYTHONS
        from pythonz.commands.locate import LocateCommand as LocatePython

        def ListPythons():
            try:
                Path(PATH_PYTHONS).mkdir(parents=True)
            except OSError:
                pass
            return ListCommand()
    except:
        # create mock commands
        InstallCommand = ListPythons = LocatePython = UninstallCommand = \
            lambda : sys.exit('You need to install the pythonz extra.  pip install pew[pythonz]')
else:
    # Pythonz does not support windows
    InstallCommand = ListPythons = LocatePython = UninstallCommand = \
        lambda : sys.exit('Command not supported on this platform')

    import shellingham



def detect_shell():
    shell = os.environ.get('SHELL', None)
    if not shell:
        if 'CMDER_ROOT' in os.environ:
            shell = 'Cmder'
        elif defaults.WINDOWS:
            try:
                _, shell = shellingham.detect_shell()
            except shellingham.ShellDetectionFailure:
                shell = os.environ.get('COMSPEC', 'cmd.exe')
        else:
            shell = 'sh'
    return shell