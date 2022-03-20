'''
This class with a configuration parser takes a scenario file and generates all variations
between components and variables that are defined within.
'''

### System modules ###
import click
from jinja2 import Environment, meta, FileSystemLoader
from pathlib import Path
from cerberus import Validator
from pprint import pformat, pprint
from itertools import product
from tomli import load
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
        self.is_valid      = True

    def __repr__(self):
        try:
            return f"{self.scenario_list[0]['name']} (valid: {self.is_valid})"
        except Exception:
            return f"{self.scenario_path} (valid: {self.is_valid})"
    
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
        """
        { 
            'dns_server': [ 'bind9.yaml', 'dnsmasq.yaml' ], 
            'dns_tunnel': [ 'iodine.yaml', 'dnscat.yaml' ] 
        }
        """
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
            self._scenario_component_product = {}
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
    def load_scenario(self) -> dict:
        """
        Reads in the scenario file and returns a dict representation.
        This function exits all execution when provided with a YAML file containing syntax errors.
        """
        logger.debug(f"Loading scenario: {self.scenario_path}")
        with open(self.scenario_path, 'r') as sp:
            try:
                scenario_dict = yaml.safe_load(sp)
                return scenario_dict
            except yaml.YAMLError as exception:
                logger.debug(f"Loaded file is not valid YAML syntax. \nFile: {self.scenario_path}\nErrors: {exception}")
                click.echo(f"[!] Loaded scenario file is an invalid YAML file ({self.scenario_path}). See debug output for more information.")
                exit(1)
                

    def validate_schema(self, scenario_dict: dict) -> bool:
        """
        Check for scenario schema validity, presence of all required fields, components etc.
        :param scenario_dict: dictionary to be validated according to the provided specification.
        """
        v =  Validator(self.schema)
        
        if scenario_dict == None:
            logger.debug(f'The provided scenario was an empty and therefore invalid.')
            return False

        if v.validate(scenario_dict):
            return True
        else:
            logger.debug(f'The scenario failed validation: {pformat(v.errors)}')
            return False


    def render_scenario(self) -> list:
        """
        Create the scenario dictionary from the provided YAML file / Jinja2 templates.
        This function is heavy on string manipulation, converting between jinja2 and YAML
        file specifications/data types to get the desired result.
        """
        # Load the scenario YAML file.
        logger.debug(f"Loading the YAML scenario file: {self.scenario_path}")
        scenario = self.load_scenario()

        # Create Jinja environment.
        env = Environment(loader=FileSystemLoader(self.scenario_parent_path))

        # Parse the scenario and find undefined Jinja variables.
        ast = env.parse(scenario)
        missing_vars = meta.find_undeclared_variables(ast)
        logger.debug(f"Missing variable(s) found: {missing_vars}")

        # Initialize list of scenario definitions.
        list_of_components = {}

        # First go over all components that need to be defined.
        for var in missing_vars:
            if var == "variables":
                continue
            
            # Test if the required component directory exists.
            p = Path(f"{self.scenario_parent_path}/{var}")
            if p.is_dir():
                logger.debug(f"Component directory exists: {p}")
                list_of_components[var] = [file for file in p.glob('*.yaml') if file.is_file()]
            else:
                logger.debug(f"Component directory does not exist. This should be fixed before the scenario can be run. Path: {p}")
                click.echo(f"Component {var} does not exist in {self.scenario_parent_path}")
                self.is_valid = False
                return
        
        # Store found components
        self.scenario_components = list_of_components
        
        # Read in the scenario definition, but strip all quotes around Jinja2 variables.
        with open(self.scenario_path, 'r') as f:
            template_string = f.read()
            template_string = template_string.replace('"{{','{{').replace('}}"','}}')
            if self.scenario_components == {}:
                template_string = template_string.replace('{{','{% raw %}{{').replace('}}','}}{% endraw %}')
                template = env.from_string(template_string)
            else:
                template = env.from_string(template_string)

        # The following block reads in the components and inserts them into the base scenario dictionary.
        int_scenario_list = []
        #fully_rendered_scenario_list = set()
        fully_rendered_scenario_list = []

        # This section is for simple scenarios without variance in components but only variables.
        if self.scenario_components == {}:
            m = template.render()
            int_scenario_list.append(m)
        else:
            for instance in self.scenario_component_product:
                template_vars = {}
                for component in self.scenario_components:
                    with open(instance[component], 'r') as f:
                        m = yaml.safe_load(f.read())
                        template_vars[component] = m

                m = template.render(template_vars)
                int_scenario_list.append(m)

        for scenario in int_scenario_list:
            # Check for missing variables
            ast = env.parse(scenario)
            missing_vars = meta.find_undeclared_variables(ast)

            # No variables are set, appending to full scenario list and moving on.
            if len(missing_vars) < 1:
                #fully_rendered_scenario_list.add(scenario)
                fully_rendered_scenario_list.append({'variables': {}, 'scenario': scenario})
                continue

            # Only allowed missing variable is 'variables'
            if missing_vars != {'variables'}:
                click.echo("[!] Some variables were found that are not listed under 'variables'. These will be ignored. Skipping this scenario.")
                logger.debug(f"All variables need to be findable under the 'variables' section. At least one was not found: {missing_vars}")
                continue

            # Load the scenario and perform final jinja variale string operation
            loaded_scenario = yaml.safe_load(scenario)
            template = env.from_string(scenario.replace('"{{','{{').replace('}}"','}}'))

            # One last iteration of the template to get the matrix between variables
            variable_list = {}
            for var in loaded_scenario['variables']:
                if self.scenario_components == {}:
                    for key,_ in var.items():
                        var = { 'name': key, 'val': [var]}
                if var['val'] == None:
                    continue
                for item in var['val']:
                    variable_list.update(item)

            keys, values = zip(*variable_list.items())                
            variable_product = [dict(zip(keys,i)) for i in product(*values)]
            
            for variable_instance in variable_product:
                template_vars = {'variables': variable_instance}
                m = template.render(template_vars)
                fully_rendered_scenario_list.append({'variables': variable_instance, 'scenario': m})


        final_list = []
        list_of_seen_scenarios = []
        error_message_displayed = False
        for scenario in fully_rendered_scenario_list:
            scenario_loaded = yaml.safe_load(scenario['scenario'])
            # Validating the final loaded scenario
            if self.validate_schema(scenario_loaded):
                scenario_loaded.pop('variables', True)
                if scenario_loaded in list_of_seen_scenarios:
                    continue
                final_list.append({'variables': scenario['variables'], 'scenario': scenario_loaded})
                list_of_seen_scenarios.append(scenario_loaded)
                logger.debug(f"Scenario is valid: {self.scenario_path}. Set variables: {scenario['variables']}")
            else:
                logger.debug(f"A Scenario instance was found to be invalid.")
                if not error_message_displayed:
                    click.echo(f"\t[!] At least one given scenario variation was found to be invalid ({self.scenario_path}). Please see debug log for more verbose output.")
                    logger.debug(f"Invalid scenario: {self.scenario_path}")
                    error_message_displayed = True
                self.is_valid = False
                continue

        self.scenario_list = final_list
        return self.scenario_list