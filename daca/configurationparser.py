'''
This configuration parser takes a scenario file and generates all subversions
which can be created.
'''

### System modules ###
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

### Local modules ###

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class Scenario:
    def __init__(self,
                 scenario_path: Path,
                 scenario_id: int
                ) -> None:
        self.scenario_path = scenario_path
        self.scenario_id   = scenario_id
        self.scenario_name = scenario_path.name
    
    ### Static methods ###
    @staticmethod
    def validate_scenario(self):
        """
        Check for scenario schema validity, presence of all components etc.
        """
        pass

    ### Properties ###
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


class ConfigurationParser:
    def __init__(self, scenario=None) -> None:
        # Read in Jinja templates
        print(Path(__file__).parent)
        loader = FileSystemLoader(f"{Path(__file__).parent.absolute()}/templates", 
                                  encoding='utf8')
        self._jinja_env = Environment(loader=loader, 
                                      autoescape=select_autoescape())
        print(self._jinja_env.list_templates())

        self.list_scenarios()
        self.list_scenarios("/home/japie/Desktop/thesis/DACA/scenarios/")
        #t = self._jinja_env.get_template("child1.html")
        #print(template.render(the="variables", go="here"))
        #print(t.render())


    ### Properties ###
    @property
    def scenario(self):
        return self._scenario
    
    @scenario.setter
    def scenario(self, scenario):
        self._scenario = scenario


    def list_scenarios(self, path=None):
        """
        Lists out-of-the-box scenarios.
        """
        if path == None:
            path = Path(f"{(Path(__file__).parent).parent}/scenarios/")
        else:
            path = Path(path)

        scenarios = path.glob('*/*yaml*')
        scenario_list = [i for i in scenarios if i.is_file()]
        scenario_list.sort()

        for scenario in scenario_list:
            # 1. Validate if scenario is valid
            scenario_is_valid = Scenario.validate_scenario(scenario)
            # 2. Print all found scenarios
            if scenario_is_valid:
                print(f"[{scenario_list.index(scenario)}]\t{scenario.name}")
            else:
                print(f"[{scenario_list.index(scenario)}]\t{scenario.name} (Invalid scenario)")

        dirs = [d for d in path.iterdir() if (d.is_dir() and not d.name.startswith('__'))]
        for d in dirs:
            print(d.name)