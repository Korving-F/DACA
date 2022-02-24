'''
This scenario runner takes a playbook generated by the
'''
# System modules
import yaml
import jinja2
from pathlib import Path

# Local modules
import scenarios
from .vagrantcontroller   import VagrantController
from .terraformcontroller import TerraformController
from .dockercontroller    import DockerController
from .configurationparser import ConfigurationParser

# Setup logging
import logging
logger = logging.getLogger('daca')

class Scenario:
    def __init__(self,
                 scenario_path: Path=None
                ) -> None:
        self.scenario_path = scenario_path
        self.available_scenarios = scenario_path
    
    ### Static methods ###
    @staticmethod
    def validate_scenario(path: Path):
        """
        Check for scenario schema validity, presence of all components etc.
        """
        pass

    ### Properties ###
    @property
    def scenario_path(self):
        return self._scenario_path
    
    @scenario_path.setter
    def scenario_path(self, scenario_path):
        self._scenario_path = scenario_path


class ScenarioRunner:
    def __init__(self, 
                 scenario_path: str=None,
                 scenario_dir: Path=None
                ) -> None:
        self.scenario_path = scenario_path
        self.available_scenarios = self.scenario_path
        self._configuration_parser = ConfigurationParser()

    ### STATIC METHODS ###

    ### PROPERTIES ###
    @property
    def available_scenarios(self):
        return self._available_scenarios

    @available_scenarios.setter
    def available_scenarios(self, path: Path=None):
        if path == None:
            path = Path(f"{(Path(__file__).parent).parent}/scenarios/")
        scenarios = path.glob('*/*yaml*')
        scenario_list = [i for i in scenarios if i.is_file()]
        scenario_list.sort()
        self._available_scenarios = scenario_list 

    def list_scenarios(self, path: Path=None):
        """
        Lists scenarios.
        """
        logger.debug("Listing available scenarios.")
        for scenario in self.available_scenarios:
            # 1. Validate if scenario is valid
            scenario_is_valid = Scenario.validate_scenario(scenario)
            # 2. Print all found scenarios
            if scenario_is_valid:
                print(f"[{self.available_scenarios.index(scenario)}]\t{scenario.name}")
            else:
                print(f"[{self.available_scenarios.index(scenario)}]\t{scenario.name} (Invalid)")

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
    def setup(self):
        pass

    def run(self):
        pass

    #dirs = [d for d in path.iterdir() if (d.is_dir() and not d.name.startswith('__'))]
    #for d in dirs:
    #    print(d.name)