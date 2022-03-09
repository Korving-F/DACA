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
    def set_working_dir(self, working_dir: Path=None):
        '''
        Set working directory for the controller used.
        '''
        pass

    @abstractmethod
    def build_config(self, config: dict):
        '''
        Create configuration file(s) based on input scenario dictionary.
        '''
        pass