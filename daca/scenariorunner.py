'''
This 
'''

# System modules
import yaml
import jinja2
import pathlib

# Local modules
import scenarios
from .vagrantcontroller   import VagrantController
from .terraformcontroller import TerraformController
from .configurationparser import ConfigurationParser

# Setup logging
import logging
logger = logging.getLogger('daca')

class ScenarioRunner:
    def __init__(self, 
                 scenario_id: str=None, 
                 scenario_path: str=None
                
                ) -> None:
        self.scenario_id = scenario_id
        self.scenario_path = scenario_path
        self._configuration_parser = ConfigurationParser()

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
