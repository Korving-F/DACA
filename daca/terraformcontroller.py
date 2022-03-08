'''
NB! Terraform is not currently supported.
This is a placeholder class for possible future inclusion. 
'''

### Local modules ###
from .controller import Controller

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class TerraformController(Controller):
    def __init__(self) -> None:
        pass