'''
This is here to convert YAML based scenarios to build/run system specific 
target files (e.g. terraform, docker, vagrant).
'''

### System modules ###
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class ConfigurationParser:
    def __init__(self) -> None:
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