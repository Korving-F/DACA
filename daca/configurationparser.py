'''
This configuration parser takes a scenario file and generates all subversions
which can be created.
'''

# System modules
from jinja2 import Environment, PackageLoader, select_autoescape

# Local modules

# Setup logging
import logging
logger = logging.getLogger('daca')

class ConfigurationParser:
    def __init__(self) -> None:
        # Read in Jinja templates
        self._jinja_env = Environment(loader=PackageLoader('daca'),
                                      autoescape=select_autoescape())
    
    # Properties
    @property
    def scenario(self):
        return self._scenario
    
    @scenario.setter
    def scenario(self, scenario):
        self._scenario = scenario