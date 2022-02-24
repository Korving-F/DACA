#!/usr/bin/env python3
### System modules ###
from email.policy import default
import logging
from pydoc import cli
import click
from pathlib import Path

### Local modules ###
from daca import *
from daca.configurationparser import ConfigurationParser
from daca.vagrantcontroller import VagrantController
from daca.scenariorunner import ScenarioRunner

### Setup logging ###
logger = logging.getLogger('daca')

### Global Variables ###
BANNER='''
      ___           ___           ___           ___     
     /\  \         /\  \         /\  \         /\  \       
    /::\  \       /::\  \       /::\  \       /::\  \      
   /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\:\  \     
  /:/  \:\__\   /::\~\:\  \   /:/  \:\  \   /::\~\:\  \    
 /:/__/ \:|__| /:/\:\ \:\__\ /:/__/ \:\__\ /:/\:\ \:\__\   
 \:\  \ /:/  / \/__\:\/:/  / \:\  \  \/__/ \/__\:\/:/  /   
  \:\  /:/  /       \::/  /   \:\  \            \::/  /    
   \:\/:/  /        /:/  /     \:\  \           /:/  /     
    \::/__/        /:/  /       \:\__\         /:/  /      
     ~~            \/__/         \/__/         \/__/       
     v1.0 (https://github.com/Korving-F/DACA)                                                                           
'''

def set_logging(debug):
    '''
    Set logging parameters.

    Keyword arguments:
    debug -- enable debug level logging (default False)
    '''
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [ %(filename)s:%(lineno)s %(funcName)s %(levelname)s ] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    print("asd")


@click.group()
#@click.option('--debug', default=False, help='Set debug logging level.')
#@click.option('--test', default="asd", help='asd123', type=str)
def main(debug):
    set_logging(debug)
    #click.echo(test)
    #click.echo(debug)
    #x = click.prompt("ASD")
    #x = click.prompt("asd", confirmation_prompt=True)
    #click.echo(x)

@main.command()
@click.option('--path', default='scenarios', help='asd')
def scenario(path):
    click.echo("wOOp")

if __name__ == '__main__':
    # Click - determine debug level
    #set_logging()
    print(BANNER)
    main()
    # daca.py --

    # daca.py --debug --scenario /path/to/scenario.yaml
    # daca.py --list-scenarios
    # daca.py --summarize --scenario-id 1

    path = Path(r'scenarios')
    runner = ScenarioRunner(path.absolute())
    runner.list_scenarios()

    # Click - determine scenario
    #print(dns_tunnel.tralala())
    # Click - Interactive should be a flag?
    #chosen_scenario = "dns_tunnel"
    controller = VagrantController("asd")

    #for server in servers:
    #x = ScenarioRunner("asd")
    #x.run()
    #logger.info("test log")