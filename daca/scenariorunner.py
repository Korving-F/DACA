# Standard modules
import yaml
import jinja2
import pathlib

# Custom Modules
import scenarios
import templates
from .vagrantcontroller import VagrantController

class ScenarioRunner:
    def __init__(self, scenario_id: str, scenario_path: str = None) -> None:
        self.scenario_id = scenario_id
        self.scenario_path = scenario_path

    @property
    def scenario_id(self):
        return self._scenario_id

    @scenario_id.setter
    def scenario_id(self, scenario_id):
        self._scenario_id = scenario_id 

    @property
    def scenario_path(self):
        return self._scenario_path
    
    @scenario_path.setter
    def scenario_path(self, scenario_path):
        self._scenario_path = scenario_path

    def setup():
        pass

    def run(self):
        pass