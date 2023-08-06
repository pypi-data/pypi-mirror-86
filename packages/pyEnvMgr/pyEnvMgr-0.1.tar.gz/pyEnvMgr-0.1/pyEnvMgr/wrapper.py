
class Wrapper:
    def __init__(self, manager, name):
        self._mgr = manager
        self.name = name

    @property
    def absolute_path(self):
        return self._mgr.env_path(self.name)

    def activate(self):
        self._mgr.activate(self.name)