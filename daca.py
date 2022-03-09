#!/usr/bin/env python3
### System modules ###
import logging
import click
from pathlib import Path


### Local modules ###
from daca import *
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
     v0.1 (https://github.com/Korving-F/DACA)                                                                           
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


@main.command()
@click.option('--path', '-p', required=True, help='''Path to scenario definition file. 
                                                     Give "*" to delete all objects DACA can find.
                                                     Prompts for confirmation.''', type=str)
def destroy(path):
    """
    Cleans-up all scenario related objects like VMs/Docker images.
    """
    logger.debug(f"Destroying scenario with path: {path}")
    click.echo("Destroying")
    #TODO Implement cleanup


@main.command()
@click.option('--path', '-p', default='scenarios', help='Path to scenario definition file.', type=str)
@click.option('--id', '-i', help='ID of the scenario that needs to be displayed.', type=int)
@click.option('--workingdir', '-w', default='data', help='Working directory where all files are stored (e.g. VMs).', type=str)
@click.option('--datapath', '-d', help='Path where extracted data samples should be stored.', type=str)
@click.option('--interactive', is_flag=True, help='Run the scenario interactively')
#@click.option('--parralelize', '-p', help='Run the scenarios in parrlalel', type=int) # TODO
def run(path, id, workingdir, datapath, interactive):
    """
    Run the selected scenario.

    Download and build the infrastructure for the selected scenario.
    E.g. VMs, Docker containers or cloud-based infrastructure used as attack, server or 
    client machines as well as supportive components to collect data.
    """
    logger.debug(f"Running scenario with path: {path}")
    logger.debug(f"Storing data at path: {datapath}")

    click.echo("[+] Starting execution.")
    if interactive == True:
        click.echo("Run the scenario interactively.")

    runner = ScenarioRunner(scenario_path=Path(path).absolute(),
                            working_directory=Path(workingdir).absolute())

    if id != None:
        runner.set_scenario_by_id(id)

    if runner.scenario is None:
        click.echo("[!] No scenario is set to build. Please point to a file or use the '--id' flag.")
        exit(1)

    runner.run()
    

@main.command()
@click.option('--path', '-p', default='scenarios', help='Path to scenario definition file or directory.', type=str)
@click.option('--id', '-i', help='ID of the scenario that needs to be displayed.', type=int)
@click.option('--summarize', '-s', is_flag=True, help='Summarize scenario runthrough (e.g. # of cycles / approximate running time)')
@click.option('--list', '-l', is_flag=True, help='List all available scenarios')
def info(path, id, summarize, list):
    """
    Display information and metadata on available scenario(s).  
    """
    logger.debug(f"Displaying information on scenario with given path: {path}")
    if list == True:
        logger.debug(f"Listing avaiable scenarions {Path(path).absolute()}")
        runner = ScenarioRunner(Path(path).absolute())
        runner.list_scenarios()
    
    if summarize == True:
        logger.debug(f"Summarizing scenario: {Path(path).absolute()}")
        runner = ScenarioRunner(Path(path).absolute())
        if id != None:
            runner.set_scenario_by_id(id)

        if runner.scenario is None:
            click.echo("[!] No scenario is set to summarize. Please point to a file or use the '--id' flag.")
            exit(1)
        
        runner.summarize()


# Function to force print help section
#def print_help():
#    ctx = click.get_current_context()
#    click.echo(ctx.get_help())

if __name__ == '__main__':
    print(BANNER)
    main()