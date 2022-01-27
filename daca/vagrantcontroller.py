from vagrant import Vagrant

class VagrantController:
    def __init__(self, scenario) -> None:
        self._vagrant = Vagrant()
        pass

    def check_vagrant_version():
        pass

    @property
    def scenario(self, scenario):
        self._scenario = scenario