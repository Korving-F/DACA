from abc import ABC, abstractmethod

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