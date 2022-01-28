from vagrant import Vagrant

class VagrantController:
    def __init__(self) -> None:
        self._vagrant = Vagrant()
        pass

    def check_vagrant_version():
        pass

    @property
    def vagrant(self):
        return self._vagrant

    @vagrant.setter
    def vagrant(self, vagrant):
        self._vagrant = vagrant

    def something(self):
        self._vagrant.box_add()