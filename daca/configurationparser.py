'''
This configuration parser takes a scenario file and generates all variations
which can be created.
'''

### System modules ###
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import yaml

### Local modules ###

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class ConfigurationParser:
    def __init__(self, scenario_path: Path=None) -> None:
        # Read in parent Jinja templates
        loader = FileSystemLoader(f"{Path(__file__).parent.absolute()}/templates", 
                                  encoding='utf8')
        self._jinja_env = Environment(loader=loader, 
                                      autoescape=select_autoescape())
        print(self._jinja_env.list_templates())
        #t = self._jinja_env.get_template("child1.html")
        #print(template.render(the="variables", go="here"))
        #print(t.render())

        # Read in 


    ### Properties ###

    ### Helper methods ###
    def read_property(self, property):
        return yaml.load(property)