'''
This configuration parser takes a scenario file and generates all variations
which can be created.
'''

### System modules ###
from pathlib import Path
from cerberus import Validator
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
        self.scenario_path         = scenario_path
        self.schema                = scenario_schema
        self.validate_scenario()
    
    def __repr__(self):
        return f"woop: {self.scenario_path}"
    
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
    def schema(self):
        return self._schema
    
    @schema.setter
    def schema(self, schema: str):
        self._schema = schema

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name
    
    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def is_valid(self) -> bool:
        return self._is_valid
    
    @is_valid.setter
    def is_valid(self, is_valid: bool):
        self._is_valid = is_valid


    ### Helper methods ###
    def load_scenario(self):
        with open(self.scenario_path, 'r') as sp:
            try:
                return yaml.safe_load(sp)
            except yaml.YAMLError as exception:
                logger.debug(f"YAML file is not valid: {self.scenario_path}")
                raise exception

    def validate_schema(self):
        v =  Validator(self.schema)
        if v.validate(self.scenario_path):
            return True
        else:
            logger.debug(f'The scenario failed validation: {v.errors}')
            print(f'The scenario failed validation: {v.errors}')
            return False


    def validate_scenario(self) -> None:
        """
        Check for scenario schema validity, presence of all required fields, components etc.
        """
        if self.name == None:
            logger.debug(f"Scenario invalid due to missing name parameter. Scenario: {self}")
            self._is_valid = False
            return

        if self.description == None:
            logger.debug(f"Scenario invalid due to missing description parameter. Scenario: {self}")
            self._is_valid = False
            return

        logger.debug("Scenario invalid due to missing name parameter.")
        self._is_valid = True


    def read_property(self, property):
        """
        Reads in a property.
        """
        #return yaml.load(property)
        pass

    def summarize(self):
        """
        Summarizes itself: number of variations, # of components, variables etc.
        """
        pass
