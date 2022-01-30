from vagrant import Vagrant

class VagrantController:
    def __init__(self, vagrant_home: str) -> None:
        self._vagrant = Vagrant()

    def check_vagrant_version():
        pass

    @property
    def vagrant(self):
        return self._vagrant

    @vagrant.setter
    def vagrant(self, vagrant):
        self._vagrant = vagrant

    @property
    def vagrant_home(self):
        return self._vagrant_home

    @vagrant_home.setter
    def vagrant_home(self, vagrant_home):
        # Setting new HOME directory where boxes are stored.
        self._vagrant_home = vagrant_home
        os_env = os.environ.copy()
        os_env['VAGRANT_HOME'] = vagrant_home
        self._vagrant.env = os_env

    def something(self):
        self._vagrant.box_add()