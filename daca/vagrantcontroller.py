'''
Wrapper module to deal with project specific Vagrant interactions.
See also:
* https://github.com/todddeluca/python-vagrant
* https://pypi.org/project/python-vagrant/
'''
### System modules ###
import re
import os
from vagrant import Vagrant
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

### Local modules ###
from .controller import Controller

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class VagrantController(Vagrant, Controller):
    def __init__(self, **kwargs) -> None:
        logger.debug("Initiating VagrantController")
        self.vagrant = Vagrant()
        # Read in parent Jinja templates
        loader = FileSystemLoader(f"{Path(__file__).parent.absolute()}/templates", 
                                  encoding='utf8')
        self._jinja_env = Environment(loader=loader, 
                                      autoescape=select_autoescape())

    ### PROPERTIES ###
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
        '''
        Setting new HOME directory where boxes are stored.
        Can be used to store VM disks to dedicated disk or partition.
        '''
        self._vagrant_home = vagrant_home
        self._vagrant.env = self.set_env_variable('VAGRANT_HOME', vagrant_home)

    def set_working_dir(self, working_dir: Path=None):
        '''
        Validates the created configuration file(s).
        '''
        pass

    ### HELPER FUNCTIONS ###
    def set_env_variable(self, env_variable_name, env_variable_val):
        os_env = os.environ.copy()
        os_env[env_variable_name] = env_variable_val
        self._vagrant.env = os_env

    def something(self):
        self._vagrant.box_add()

    def validate(self):
        '''
        Validates the created Vagrantfile.
        '''
        output = self._vagrant._run_vagrant_command(['validate'])
        m = re.search(r'^Vagrantfile validated successfully.$', output)
        if m is None:
            raise Exception(f"Failed to parse vagrant validate output. output={output}")
        return True

    def validate_env(self):
        '''
        Validates the running environment.
        '''
        pass
    
    def check_controller_version(self):
        pass

    def build_config(self, config: dict):
        pass