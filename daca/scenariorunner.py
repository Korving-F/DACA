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
from .scenario            import Scenario

### Setup logging ###
import logging
logger = logging.getLogger('daca')


class ScenarioRunner:
    def __init__(self, 
                 scenario_path: Path=None
                ) -> None:
        self.scenario_path = scenario_path
        self.available_scenarios = self.scenario_path


    ### STATIC METHODS ###

    ### PROPERTIES ###
    @property
    def available_scenarios(self):
        return self._available_scenarios

    @available_scenarios.setter
    def available_scenarios(self, path: Path=None):
        if path == None:
            path = Path(f"{(Path(__file__).parent).parent}/scenarios/")

        # Go over subdirectories and add valid Scenarios to internal list
        dirs = [d for d in path.iterdir() if (d.is_dir() and not d.name.startswith('__'))]
        dirs.append(path)
        scenario_list = []
        for d in dirs:
            scenario_file = Path(f"{d}/{d.name}.yaml")
            if not scenario_file.is_file():
                continue
            
            scenario = Scenario(scenario_file)
            if scenario.is_valid():
                scenario_list.append(scenario)
                pass

            scenario_list.sort()

        self._available_scenarios = scenario_list

    @property
    def scenario_path(self):
        return self._scenario_path
    
    @scenario_path.setter
    def scenario_path(self, scenario_path):
        self._scenario_path = scenario_path
        self.scenario = scenario_path

    @property
    def scenario(self):
        return self._scenario
    
    @scenario.setter
    def scenario(self, scenario_path):
        self._scenario = Scenario(scenario_path)


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


    def setup(self):
        pass


    def run(self):
        pass

