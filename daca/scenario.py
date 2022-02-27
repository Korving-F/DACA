'''
This configuration parser takes a scenario file and generates all variations
which can be created.
'''

### System modules ###
from pathlib import Path
from cerberus import Validator
from pprint import pformat
import yaml

### Local modules ###
from .scenario_schema import scenario_schema


### Setup logging ###
import logging
logger = logging.getLogger('daca')


class Scenario:
    def __init__(self,
                 scenario_path: Path
                ) -> None:
        logger.debug(f"Initiating Scenario object with path: {scenario_path}")
        self.scenario_path         = scenario_path
        self.schema                = scenario_schema
        self.scenario_dict         = self.load_scenario()
        self.validate_schema()

    def __repr__(self):
        return f"woop: {self.scenario_dict['name'] if self.scenario_dict is not None else self.scenario_path} (valid: {self.is_valid})"
    
    def __lt__(self, other):
        return self.scenario_path < other.scenario_path

    ### Static methods ###


    ### Properties ###
    @property
    def scenario_path(self):
        return self._scenario_path
    
    @scenario_path.setter
    def scenario_path(self, scenario_path: Path):
        self._scenario_path = scenario_path

    @property
    def scenario_dict(self):
        return self._scenario_dict
    
    @scenario_dict.setter
    def scenario_dict(self, scenario_dict: dict):
        self._scenario_dict = scenario_dict

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema: str):
        self._schema = schema

    @property
    def is_valid(self) -> bool:
        return self._is_valid
    
    @is_valid.setter
    def is_valid(self, is_valid: bool):
        self._is_valid = is_valid


    ### Helper methods ###
    def load_scenario(self):
        logger.debug(f"Loading scenario: {self.scenario_path}")
        with open(self.scenario_path, 'r') as sp:
            try:
                scenario_dict = yaml.safe_load(sp)
                if scenario_dict == None:
                    return None
                return scenario_dict
            except yaml.YAMLError as exception:
                logger.debug(f"Loaded YAML file is not valid. \nFile: {self.scenario_path}\nErrors: {exception}")
                print(f"[!] Loaded scenario file is invalid: {self.scenario_path}")
                return None
                

    def validate_schema(self):
        """
        Check for scenario schema validity, presence of all required fields, components etc.
        """
        v =  Validator(self.schema)
        
        if self.scenario_dict == None:
            self.is_valid = False
            return

        if v.validate(self.scenario_dict):
            self.is_valid = True
        else:
            logger.debug(f'The scenario failed validation: {pformat(v.errors)}')
            self.is_valid = False
            return v.errors


    def render_scenarios(self):
        """
        TODO: these are results for first experiments with dict/jinja2 inheritance.
        """
        import yaml
        import pprint
        from jinja2 import Environment, meta, DictLoader, FileSystemLoader, Template

        def load_scenario(file):
            with open(file, 'r') as sp:
                try:
                    scenario_dict = yaml.safe_load(sp)
                    if scenario_dict == None:
                        return None
                    return scenario_dict
                except yaml.YAMLError as exception:
                    print(f"[!] Loaded scenario file is invalid: {file}")
                    return None


        x = load_scenario("dns_tunnel/dns_tunnel.yaml")
        env = Environment(loader=FileSystemLoader('dns_tunnel/'))
        ast = env.parse(x)
        y = meta.find_undeclared_variables(ast)
        print(y)

        with open(f'dns_tunnel/dns_server/bind9.yaml', 'r') as sp:
            dns_server = { 'dns_server': yaml.safe_load(sp) }

        with open(f'dns_tunnel/dns_tunnel/bind9.yaml', 'r') as sp:
            dns_tunnel = { 'dns_tunnel': yaml.safe_load(sp)}

        template = env.get_template('dns_tunnel.yaml')
        m = template.render(dns_server=dns_server['dns_server'], dns_tunnel=dns_tunnel['dns_tunnel'])
        pprint.pprint(yaml.safe_load(m))



    def read_property(self, property):
        """
        Reads in a property.
        """
        return self.scenario_dict[property]


    def summarize(self):
        """
        Summarizes itself: number of variations, # of components, variables etc.
        """
        pass
