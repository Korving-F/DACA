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
from jinja2 import Environment, FileSystemLoader, select_autoescape, meta

### Local modules ###
from .controller import Controller

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class VagrantController(Vagrant, Controller):
    def __init__(self, **kwargs) -> None:
        logger.debug("Initiating VagrantController")
        self.vagrant = Vagrant()
        self.jinja_env = None

    ### PROPERTIES ###
    @property
    def vagrant(self):
        return self._vagrant

    @vagrant.setter
    def vagrant(self, vagrant: Vagrant):
        self._vagrant = vagrant

    @property
    def jinja_env(self):
        return self._jinja_env

    @jinja_env.setter
    def jinja_env(self, jinja_env: Environment):
        self._jinja_env = jinja_env

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

    def set_working_directory(self, working_dir: Path):
        '''
        Set the working directory where vagrant will look for 
        '''
        self.set_env_variable('VAGRANT_CWD', working_dir)

    ### HELPER FUNCTIONS ###
    def set_env_variable(self, env_variable_name: str, env_variable_val: str):
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


    def build_config(self, config: dict, scenario_dir: Path, data_dir: Path):
        loader = FileSystemLoader(f"{Path(__file__).parent.absolute()}/templates", encoding='utf8')
        self.jinja_env = Environment(loader=loader, autoescape=select_autoescape())

        # Parse the scenario and find undefined Jinja variables.
        ast = self._jinja_env.parse(config)
        missing_vars = meta.find_undeclared_variables(ast)
        logger.debug(f"Missing variable(s) found: {missing_vars}")

        # Go over each component and build VM config
        vm_dict = {'scenario_vms': []}
        for component in config['scenario']['components']:
            component_dict = component
            component_dict['hostname'] = component_dict['name'].strip().lower().replace(' ','').replace('_','')
            component_dict['dest_path'] = f"{data_dir}/{component_dict['hostname']}/"

            template = self._jinja_env.get_template('VagrantVM.j2')
            m = template.render(component_dict)
            vm_dict['scenario_vms'].append(m)
        
        template = self._jinja_env.get_template('Vagrantfile.j2')
        m = template.render(vm_dict)
        with open(f"{scenario_dir}/Vagrantfile", "w") as f:
            f.write(m)

        self.validate()