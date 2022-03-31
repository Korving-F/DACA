'''
This class takes a scenario description and executes it. 
'''
### System modules ###
from typing import Dict, Any
from datetime import datetime
import psutil
import hashlib
import json
from pathlib import Path
from pprint import pprint
import click

### Local modules ###
from .vagrantcontroller   import VagrantController
from .terraformcontroller import TerraformController
from .dockercontroller    import DockerController
from .scenario            import Scenario

### Setup logging ###
import logging
logger = logging.getLogger('daca')


class ScenarioRunner:
    def __init__(self, 
                 scenario_path: Path=None,
                 working_directory: Path=None,
                 quiet: bool=False,
                 interactive: bool=False
                ) -> None:
        self.scenario_path = scenario_path
        self.scenario = None
        self.scenario_rendered = False
        self.available_scenarios = self.scenario_path
        self.controller = None
        self.configuration_parser = None
        self.working_directory = working_directory
        self.interactive = interactive


    ### STATIC METHODS ###
    @staticmethod
    def dict_hash(dictionary: Dict[str, Any]) -> str:
        """
        MD5 hash of a dictionary.
        Source: https://www.doc.ic.ac.uk/~nuric/coding/how-to-hash-a-dictionary-in-python.html (Retrieved 09.03.2022)
        """
        dhash = hashlib.md5()
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()


    ### PROPERTIES ###
    @property
    def available_scenarios(self):
        return self._available_scenarios

    @available_scenarios.setter
    def available_scenarios(self, path: Path=None):
        if path == None:
            path = Path(f"{(Path(__file__).parent).parent}/scenarios/")

        scenario_list = []
        # If pointing to a scenario file directlty
        if path.is_file() and not path.is_dir():
            logger.debug(f"Setting scenario: {path}")
            scenario = Scenario(path)
            scenario_list.append(scenario)
            self.scenario = scenario
        # Go over subdirectories and add valid Scenarios to internal list
        else:
            dirs = [d for d in path.iterdir() if (d.is_dir() and not d.name.startswith('__'))]
            dirs.append(path)
            for d in dirs:
                scenario_file = Path(f"{d}/{d.name}.yaml")
                if not scenario_file.is_file():
                    continue

                logger.debug(f"Adding scenario_file to available scenarios: {scenario_file}")
                scenario = Scenario(scenario_file)
                scenario_list.append(scenario)

        scenario_list.sort()
        self._available_scenarios = scenario_list

    @property
    def scenario_path(self):
        return self._scenario_path
    
    @scenario_path.setter
    def scenario_path(self, scenario_path):
        self._scenario_path = scenario_path

    @property
    def working_directory(self):
        return self._working_directory
    
    @working_directory.setter
    def working_directory(self, working_directory):
        self._working_directory = working_directory

    @property
    def scenario(self):
        return self._scenario
    
    @scenario.setter
    def scenario(self, scenario: Scenario):
        self._scenario = scenario

    def set_scenario_by_id(self, id: int):
        if id > len(self.available_scenarios) - 1:
            click.echo(f"[!] Scenario with ID {id} not available.")
            return
        self._scenario = self.available_scenarios[id]
        self.scenario_path = self._scenario.scenario_path

    @property
    def scenario_rendered(self):
        return self._scenario_rendered
    
    @scenario_rendered.setter
    def scenario_rendered(self, scenario_rendered: bool):
        self._scenario_rendered = scenario_rendered

    @property
    def controller(self):
        return self._controller
    
    @controller.setter
    def controller(self, controller: str):
        self._controller = controller

    @property
    def controller_type(self):
        return self._controller_type
    
    @controller_type.setter
    def controller_type(self, controller_type: str):
        self._controller_type = controller_type
        if controller_type == "vagrant":
            self.controller = VagrantController()
        elif controller_type == "docker":
            self.controller = DockerController()
        elif controller_type == "terraform":
            self.controller = TerraformController()
    
    @property
    def interactive(self):
        return self._interactive

    @interactive.setter
    def interactive(self, interactive: bool):
        self._interactive = interactive

    ### HELPER FUNCTIONS ###
    def set_controller_env_variable(self, var_name, var_value):
        if self.controller_type == 'vagrant':
            var_name = 'VAGRANT_CWD' if var_name == "CWD" else var_name
            var_name = 'VAGRANT_HOME' if var_name == "HOME" else var_name
        self.controller.set_env_variable(var_name, var_value)

    def list_scenarios(self):
        """
        Lists scenarios.
        """
        logger.debug("Listing available scenarios.")
        if len(self.available_scenarios) == 0:
            logger.debug(f"No scenarios identified under: {self.scenario_path}")
            click.echo(f"[-] No scenarios identified under: {self.scenario_path}")
            return

        click.echo("[+] Identified Scenarios:")
        for scenario in self.available_scenarios:
            scenario.render_scenario()
            print(f"\t[{self.available_scenarios.index(scenario)}] {scenario}")

    def summarize(self, id=None):
        """
        Summarizes itself: number of variations, # of components, variables etc.
        """
        self.scenario.render_scenario()
        self.scenario_rendered = True
        click.echo(f"[+] Summarizing runthrough of the following scenario: '{self.scenario}'")
        click.echo(f"[+] Discovered file-based components: {'-' if len(self.scenario.scenario_components) == 0 else ''}")
        for component in self.scenario.scenario_components:
            click.echo(f"\t[*] {component}")
            for item in self.scenario.scenario_components[component]:
                click.echo(f"\t\t[-] {item}")

        click.echo(f"[+] The product between these gives a total of {len(self.scenario.scenario_component_product)} Component combinations.")
        click.echo(f"[+] With variables included a total of {len(self.scenario.scenario_list)} runthroughs will be executed.")
        if len(self.scenario.scenario_list) > 0:
            click.echo(f"[+] Provisioner type is '{self.scenario.scenario_list[0]['scenario']['provisioner']}'.")


    def run(self):
        """
        Build / deploy defined infrastructure.
        In case variables were used inside any of the 'setup'-sections of the scenario, 
        this step will be repeated during the running.
        """   
        self.scenario.render_scenario()
        self.scenario_rendered = True

        if len(self.scenario.scenario_list) == 0:
            click.echo(f"[!] No valid scenarios found to build. Terminating")
            exit()

        # TODO: add health check for Vagrant version etc.  
        controller_type = self.scenario.scenario_list[0]['scenario']['provisioner']
        self.controller_type = controller_type

        # Create working directory and all parent directories if not exists.
        click.echo(f"[+] Creating main working directory if not exists: {self.working_directory}")
        self.working_directory.mkdir(parents=True, exist_ok=True)

        scenario_data_directory = Path(f"{self.working_directory}/{self.scenario.scenario_list[0]['scenario']['name'].strip().lower().replace(' ','_')}").absolute()
        click.echo(f"[+] Creating scenario sub-directory if not exists: {scenario_data_directory}")
        scenario_data_directory.mkdir(parents=True, exist_ok=True)
        self.controller.set_working_directory(scenario_data_directory)

        click.echo(f"[+] Running {len(self.scenario.scenario_list)} scenarios with {len(self.scenario.scenario_list[0]['scenario']['components'])} file-based components.")

        # Disk and memory availability
        disk = psutil.disk_usage(scenario_data_directory)
        click.echo(f"[+] Disk usage for chosen partition/directory ({scenario_data_directory}): \n\tTotal: {disk.total // (2**30)} GiB\n\tUsed:  {disk.used // (2**30)} GiB\n\tFree:  {disk.free // (2**30)} GiB")
        memory = psutil.virtual_memory()
        click.echo(f"[+] Memory usage on current system:\n\tTotal: {memory.total // (2**30)} GiB\n\tUsed:  {memory.used // (2**30)} GiB\n\tAvailable:  {memory.available // (2**30)} GiB")
       
        # Confirmation before proceding with runthrough
        if self.interactive:
            click.echo()
            click.echo(f"[+] Running in interactive mode. Please press CTRL-C to interrupt when you're ready to stop.")
            self.controller.print_interactive_mode_instructions(self.scenario.scenario_list[0], scenario_data_directory)
            click.echo()

        response = click.prompt("[!] Are you sure you want to start running this scenario? (y/n)", confirmation_prompt=False)
        if response.lower() not in ['yes', 'y']:
            click.echo(f"[!] Exiting scenario execution.")
            exit()
        
        # TODO: multithreading would happen here but click progressbar does not support that.
        # Alternative with multithreading support: https://github.com/tqdm/tqdm
        with click.progressbar(self.scenario.scenario_list) as bar:
            for scenario in bar:
                click.echo()
                # Create an artifact directory for a single instance of the scenario 
                instance_data_directory = Path(f"{scenario_data_directory}/{self.dict_hash(scenario)}").absolute()
                instance_data_directory.mkdir(parents=True, exist_ok=True)

                # Define metadata files for the runthrough
                instance_data_ready_file = Path(f"{instance_data_directory}/.finished").absolute()
                instance_data_metadata_file = Path(f"{instance_data_directory}/.metadata").absolute()

                if instance_data_ready_file.exists():
                    logger.debug(f"Scenario instance was already executed before, skipping: {instance_data_ready_file}")
                    continue                       

                with open(instance_data_metadata_file, 'w') as f:
                    f.write(f"execution_time: {datetime.now()}\n\n")
                    f.write(f"variables: {json.dumps(scenario['variables'])}\n\n")
                    f.write(f"scenario: {json.dumps(scenario['scenario'])}\n\n")

                click.echo(f"\t[+] Scenario Name: {scenario['scenario']['name']}")
                click.echo(f"\t[+] Variables used: {scenario['variables']}")
                click.echo(f"\t[+] Files saved under: {instance_data_directory}")

                for component in scenario['scenario']['components']:
                    if component['artifacts_to_collect'] != None:
                        component_data_directory = Path(f"{instance_data_directory}/{component['name'].strip().lower().replace(' ','').replace('_','')}").absolute()
                        component_data_directory.mkdir(parents=True, exist_ok=True)

                # Let the controller build the needed configurations and validate it.
                self.controller.build_config(scenario, scenario_data_directory, instance_data_directory, self.scenario.scenario_parent_path)
                self.controller.validate()

                # Let the controller run the configuration file
                self.controller.run(self.interactive)

                # Create finished metadata file
                with open(instance_data_ready_file, 'w') as f:
                    f.write(f"finished_time: {datetime.now()}")