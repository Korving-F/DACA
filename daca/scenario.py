'''
This configuration parser takes a scenario file and generates all variations
which can be created.
'''

### System modules ###
import click
from jinja2 import ChainableUndefined, DebugUndefined, Environment, meta, DictLoader, FileSystemLoader, Template
from pathlib import Path
from cerberus import Validator
from pprint import pformat, pprint
from itertools import product
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
        self.scenario_path = scenario_path
        self.schema        = scenario_schema
        self.scenario_list = None

    def __repr__(self):
        return f"{self.scenario_path}"
        #return f"woop: {self.scenario_dict['name'] if self.scenario_dict is not None else self.scenario_path} (valid: {self.is_valid})"
    
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
        self.scenario_parent_path = scenario_path.parent

    @property
    def scenario_parent_path(self):
        return self._scenario_parent_path
    
    @scenario_parent_path.setter
    def scenario_parent_path(self, scenario_parent_path: Path):
        self._scenario_parent_path = scenario_parent_path

    @property
    def scenario_components(self):
        return self._scenario_components
    
    @scenario_components.setter
    def scenario_components(self, scenario_components: dict):
        # { 'dns_server': [ 'bind9.yaml', 'dnsmasq.yaml' ], dns_tunnel: ['iodine.yaml', 'dnscat.yaml'] }
        self._scenario_components = scenario_components
        self.scenario_component_product = scenario_components

    @property
    def scenario_component_product(self):
        return self._scenario_component_product
    
    @scenario_component_product.setter
    def scenario_component_product(self, scenario_components: dict):
        """
        [
            {'dns_server': PosixPath('bind9.yaml'),   'dns_tunnel': PosixPath('iodine.yaml')},
            {'dns_server': PosixPath('bind9.yaml'),   'dns_tunnel': PosixPath('dnscat.yaml')},
            {'dns_server': PosixPath('dnsmasq.yaml'), 'dns_tunnel': PosixPath('iodine.yaml')},
            {'dns_server': PosixPath('dnsmasq.yaml'), 'dns_tunnel': PosixPath('dnscat.yaml')}
        ]
        """
        if len(scenario_components) == 0:
            self._scenario_component_product = None
        else:
            keys, values = zip(*scenario_components.items())                
            self._scenario_component_product = [dict(zip(keys,i)) for i in product(*values)]

    @property
    def scenario_list(self):
        return self._scenario_list
    
    @scenario_list.setter
    def scenario_list(self, scenario_list: list):
        self._scenario_list = scenario_list

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
                return scenario_dict
            except yaml.YAMLError as exception:
                logger.debug(f"Loaded file is not valid YAML syntax. \nFile: {self.scenario_path}\nErrors: {exception}")
                print(f"[!] Loaded scenario file is an invalid YAML file: {self.scenario_path}")
                exit(1)
                

    def validate_schema(self, scenario_dict: dict) -> bool:
        """
        Check for scenario schema validity, presence of all required fields, components etc.
        validate payload against a Cerberus schema
        :param payload: payload to be validated
        :return: nothing
        """
        v =  Validator(self.schema)
        
        if scenario_dict == None:
            self.is_valid = False
            return False

        if v.validate(scenario_dict):
            self.is_valid = True
            return True
        else:
            logger.debug(f'The scenario failed validation: {pformat(v.errors)}')
            self.is_valid = False
            return False


    def render_scenario(self):
        """
        Create the dictionary from YAML file / Jinja2 template
        """
        # Load the scenario YAML file
        logger.debug(f"Loading the YAML scenario file: {self.scenario_path}")
        scenario = self.load_scenario()

        # Create Jinja environment
        env = Environment(loader=FileSystemLoader(self.scenario_parent_path),undefined=ChainableUndefined)

        # Parse the scenario and find undefined variables related to components
        ast = env.parse(scenario)
        missing_vars = meta.find_undeclared_variables(ast)
        logger.debug(f"Missing variable(s) found: {missing_vars}")

        # Initialize list of scenario definitions.
        list_of_components = {}

        # First go over all components that need to be defined.
        for var in missing_vars:
            if var == "variables":
                continue
            
            # test if component dir exists
            p = Path(f"{self.scenario_parent_path}/{var}")
            if p.is_dir():
                logger.debug(f"Component directory exists: {p}")
                list_of_components[var] = [file for file in p.glob('*.yaml') if file.is_file()]
            else:
                logger.debug(f"Component directory does not exist. This should be fixed before the scenario can be run. Path: {p}")
                click.echo(f"Component {var} does not exist in {self.scenario_parent_path}")
                self.is_valid = False
                return
        
        with open(self.scenario_path, 'r') as f:
            template = env.from_string(f.read().replace('"',''))

        self.scenario_components = list_of_components

        scenario_list = []
        for instance in self.scenario_component_product:
            template_vars = {}
            for component in self.scenario_components:
                with open(instance[component], 'r') as f:
                    template_vars[component] = yaml.safe_load(f.read())

            m = template.render(template_vars)
            m_loaded = yaml.safe_load(m)
            self.validate_schema(m_loaded)
            
            if self.is_valid:
                scenario_list.append(m_loaded)
                logger.debug(f"Scenario is valid: {instance}")
            else:
                logger.debug(f"A Scenario instance was found to be invalid: {instance}")
                continue