'''
This class takes a scenario description and executes it. 
'''
### System modules ###
from pathlib import Path
import click

### Local modules ###
from .vagrantcontroller   import VagrantController
from .terraformcontroller import TerraformController
from .dockercontroller    import DockerController
from .configurationparser import ConfigurationParser
from .scenario            import Scenario

### Setup logging ###
import logging
logger = logging.getLogger('daca')


class ScenarioRunner:
    def __init__(self, 
                 scenario_path: Path=None
                ) -> None:
        self.scenario_path = scenario_path
        self.scenario = None
        self.available_scenarios = self.scenario_path
        #controller = VagrantController("asd")


    ### STATIC METHODS ###

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
    def scenario(self):
        return self._scenario
    
    @scenario.setter
    def scenario(self, scenario: Scenario):
        self._scenario = scenario

    def set_scenario_by_id(self, id: int):
        if id >= len(self.available_scenarios) - 1:
            click.echo(f"[!] Scenario with ID {id} not available.")
            return
        self._scenario = self.available_scenarios[id]

    ### HELPER FUNCTIONS ###
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
            print(f"\t[{self.available_scenarios.index(scenario)}] {scenario}")

    def summarize(self, id=None):
        """
        Summarizes itself: number of variations, # of components, variables etc.
        """
        click.echo(f"[+] Summarizing runthrough of the following scenario: {self.scenario}")
        self.scenario.render_scenario()

        click.echo(f"[+] Discovered Components:")
        for component in self.scenario.scenario_components:
            click.echo(f"\t[*] {component}")
            for item in self.scenario.scenario_components[component]:
                click.echo(f"\t\t[-] {item}")

        click.echo(f"[+] Product gives a total of {len(self.scenario.scenario_component_product)} Component combinations.")


    def build(self):
        """
        Build / deploy defined infrastructure.
        """
        pass


    def setup(self):
        """
        
        """
        pass


    def run(self):
        """
        
        """
        pass

