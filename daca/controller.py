from abc import ABC, abstractmethod
from pathlib import Path

class Controller(ABC):
    
    @abstractmethod
    def check_controller_version(self):
        '''
        Check the version of the installed controller (e.g. docker -v / ).
        '''
        pass

    @abstractmethod
    def validate(self):
        '''
        Validates the created configuration file(s).
        '''
        pass

    @abstractmethod
    def build_config(self, config: dict):
        '''
        Create configuration file(s) based on input scenario dictionary.
        '''
        pass

    @abstractmethod
    def set_env_variable(self, env_variable_name: str, env_variable_val: str):
        '''
        Set environmental variables needed by the controller / provisioner.
        E.g. working directory,
        '''
        pass

    @abstractmethod
    def set_working_directory(self, working_dir: Path):
        '''
        Set environmental variables needed by the controller / provisioner.
        E.g. working directory,
        '''
        pass

    @abstractmethod
    def run(self, interactive: bool):
        '''
        Run the configuration file.
        '''
        pass

    @abstractmethod
    def interrupt_handler(self):
        '''
        Handle a soft shutdown of the scenario when interrupted.
        This function will also be called in interactive mode.
        '''
        pass

    @abstractmethod
    def print_interactive_mode_instructions(self):
        '''
        Print instructions on how to enter the various machines in the scenario.
        '''
        pass