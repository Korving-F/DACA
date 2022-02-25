#!/usr/bin/env python3
### System modules ###
import logging
import click
from pathlib import Path


### Local modules ###
from daca import *
from daca.configurationparser import ConfigurationParser
from daca.vagrantcontroller import VagrantController
from daca.scenariorunner import ScenarioRunner


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


### Setup logging ###
logger = logging.getLogger('daca')

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


### CLI Application ###
@click.group()
@click.option('--debug', is_flag=True, help='Set debug logging level.')
def main(debug):
    set_logging(debug)
    #import time
    #with click.progressbar(["a","b","c","d"]) as bar:
    #    for foo in bar:
    #        print(foo)
    #        time.sleep(1)

    #x = click.prompt("ASD")
    #x = click.prompt("asd", confirmation_prompt=True)


@main.command()
@click.option('--path', '-p', help='Path to scenario definition file.', type=str)
def build(path):
    """
    Download and build the infrastructure for the selected scenario.
    E.g. VMs, Docker containers or cloud-based infrastructure used as attack, server or 
    client machines as well as supportive components to collect data.
    """
    logger.debug(f"Building scenario with path: {path}")
    click.echo("wOOp")


@main.command()
@click.option('--path', help='Path to scenario definition file or directory.', type=str)
@click.option('--datapath', help='Path where extracted data samples should be stored.', type=str)
def run(path, datapath):
    """
    Run the selected scenario.
    """
    logger.debug(f"Running scenario with path: {path}")
    click.echo("[+] Starting execution.")


@main.command()
@click.option('--path', default='scenarios', help='Path to scenario definition file or directory.', type=str)
@click.option('--summarize', is_flag=True, help='Summarize scenario runthrough (e.g. # of cycles / approximate running time)')
@click.option('--list', is_flag=True, help='List all available scenarios')
def info(path, summarize, list):
    """
    Display information and metadata on available scenario(s).  
    """
    logger.debug(f"Displaying information on scenario with given path: {path}")
    if list == True:
        logger.debug(f"Listing avaiable scenarions {Path(path).absolute()}")
        runner = ScenarioRunner(Path(path).absolute())
        runner.list_scenarios()


if __name__ == '__main__':
    print(BANNER)
    main()


    # daca.py --debug --scenario /path/to/scenario.yaml
    # daca.py --list-scenarios
    # daca.py --summarize --scenario-id 1


    # Click - determine scenario
    #print(dns_tunnel.tralala())
    # Click - Interactive should be a flag?
    #chosen_scenario = "dns_tunnel"
    controller = VagrantController("asd")

    #for server in servers:
    #x = ScenarioRunner("asd")
    #x.run()
    #logger.info("test log")