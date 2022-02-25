'''
This configuration parser takes a scenario file and generates all variations
which can be created.
'''

### System modules ###
from pathlib import Path

### Local modules ###
from .configurationparser import ConfigurationParser
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
        print(self.schema)
        self._configuration_parser = ConfigurationParser(scenario_path)
        self.name                  = self._configuration_parser.read_property('name')
        self.description           = self._configuration_parser.read_property('name')

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