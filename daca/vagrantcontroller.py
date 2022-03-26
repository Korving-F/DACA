'''
Wrapper module to deal with project specific Vagrant interactions.
See also:
* https://github.com/todddeluca/python-vagrant
* https://pypi.org/project/python-vagrant/
'''
### System modules ###
import re
import os
import subprocess
import click
import shutil
import signal
from vagrant import Vagrant
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape, meta
from threading import Event


### Local modules ###
from .controller import Controller

### Setup logging ###
import logging
logger = logging.getLogger('daca')

### Setup interrupt ###
exit_event = Event()

class VagrantController(Vagrant, Controller):
    def __init__(self) -> None:
        logger.debug("Initiating VagrantController")
        if logger.level == 10:
            quiet_stderr = False
            quet_stdout = False
        else:
            quiet_stderr = True
            quet_stdout = True
        self.vagrant = Vagrant(quiet_stderr=quiet_stderr, quiet_stdout=quet_stdout)
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

    def validate(self):
        '''
        Validates the created Vagrantfile.
        '''
        try:
            output = self._vagrant._run_vagrant_command(['validate'])
            m = re.search(r'^Vagrantfile validated successfully.$', output)
            if m is not None:
                return False
            return True
        except subprocess.CalledProcessError as err:
            click.echo(f"\t[!] {err}")
            return False     


    def validate_env(self):
        '''
        Validates the running environment. E.g. Vagrant version etc.
        '''
        pass

    def check_controller_version(self):
        pass

    def interrupt_handler(self, signum, frame):
        '''
        Handles a user interrupt during scenario execution so an attempt can be made to have a soft-shutdown.
        This function is also used for evidence collection in interactive session.
        '''
        click.echo()
        response = click.prompt("[!] Ctrl-c was pressed. Do you really want to exit? (y/n)")
        if response.lower() in ['yes', 'y']:
            click.echo(f"[!] Exiting scenario execution.")
            click.echo(f"[!] Collecting data. Please wait while scenario is being softly shut-down.")
            self.vagrant.halt()
            exit_event.set()
            exit()
    
    def print_interactive_mode_instructions(self, config: dict, scenario_dir: Path,):
        click.echo(f"\t[+] To interact within the scenario please execute the following in a separate shell:")
        click.echo(f"\t[+] cd {scenario_dir}")
        for component in config['scenario']['components']:
            hostname = component['name'].strip().lower().replace(' ','').replace('_','')
            click.echo(f"\t[+] vagrant ssh {hostname}")

    def build_config(self, config: dict, scenario_dir: Path, data_dir: Path, original_dir: Path):
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

            # Render and write filebeat playbook(s). NB! These conflict with each other and only one should be used (1 output for filebeat only)
            for artifact in component["artifacts_to_collect"]: 
                if artifact['type'] in ["filebeat","elastic","kafka"]:
                    template = self.jinja_env.get_template('filebeat_playbook.j2')
                    m = template.render(component_dict)
                    with open(f"{scenario_dir}/filebeat_playbook_{component_dict['hostname']}", "w") as f:
                        f.write(m)
                    with open(f"{data_dir}/filebeat_playbook_{component_dict['hostname']}", "w") as f:
                        f.write(m)

        
        # Grab the Vagrant template, render it and write to data / scenario directories
        template = self._jinja_env.get_template('Vagrantfile.j2')
        m = template.render(vm_dict)
        with open(f"{scenario_dir}/Vagrantfile", "w") as f:
            f.write(m)
        with open(f"{data_dir}/Vagrantfile", "w") as f:
            # Remove instance string
            path_string_to_remove = f"{data_dir}/"
            for line in m.split('\n'):
                if path_string_to_remove in line:
                    line = line.replace(path_string_to_remove, '')
                f.write(line + '\n')

        # Write any scripts to the scenario / data directories
        # Go over scenario to copy over replace ansible/script provisioners
        for component in config['scenario']['components']:
            if component["setup"]["type"] in ["script", "ansible"]:
                # find file and change assignment to full path
                for p in original_dir.rglob("*"):
                    if p.name == component["setup"]["val"]:
                        shutil.copy(p, data_dir)
                        shutil.copy(p, scenario_dir)
            if component["run"]["type"] in ["script"]:
                # find file and change assignment to full path
                 for p in original_dir.rglob("*"):
                    if p.name == component["run"]["val"]:
                        shutil.copy(p, data_dir)
                        shutil.copy(p, scenario_dir)
        

    def run(self, interactive: bool):
        '''
        Brings up/down the defined VMs and handles interactive session flag.
        '''
        # Two approaches are possible:
        # 1. Snapshot push/pop to restore initial state after.
        # 2. Simple restarts between scenario executions.

        # The former is more accurate, but adds complexity orchestrating the runthroughs.
        # The latter has the potentiality to have false artifact buildups (e.g. scenario1 leaves files/log entries that are reported under scenario2)

        #if previous_components.setup == current_component.setup:
        #    self.controller.snapshot_pop()
        #    self.controller.snapshot_push()
        #    self.controller.snapshot_save(name="base")
        #    self.controller.snapshot_restore(name="base")

        # Registering signal handler for interrupt
        signal.signal(signal.SIGINT, self.interrupt_handler)

        self.vagrant.up()

        if interactive:
            while not exit_event.is_set():
                exit_event.wait(60)

        self.vagrant.halt()