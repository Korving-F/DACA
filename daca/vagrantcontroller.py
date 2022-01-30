'''
Wrapper module to deal with 
'''

import subprocess
import re
import os

from vagrant import Vagrant

class VagrantController:
    def __init__(self, vagrant_home: str) -> None:
        self._vagrant = Vagrant()



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
        # Setting new HOME directory where boxes are stored.
        self._vagrant_home = vagrant_home
        self._vagrant.env = self.set_env_variable('VAGRANT_HOME', vagrant_home)

    ### HELPER FUNCTIONS ###
    def set_env_variable(self, env_variable_name, env_variable_val):
        os_env = os.environ.copy()
        os_env[env_variable_name] = env_variable_val
        self._vagrant.env = os_env

    def something(self):
        self._vagrant.box_add()

    def check_vagrant_version(self):
        pass

    def validate(self):
        '''
        Validates the created Vagrantfile.
        '''
        output = self._vagrant._run_vagrant_command(['validate'])
        m = re.search(r'^Vagrantfile validated successfully.$', output)
        if m is None:
            raise Exception(f"Failed to parse vagrant validate output. output={output}")
        return True