#!/usr/bin/env python3
# System modules
import logging
import subprocess
import shutil
import docker
from pathlib import Path

# Local modules
from daca import *
from daca.configurationparser import ConfigurationParser
from daca.vagrantcontroller import VagrantController
from daca.scenariorunner import ScenarioRunner
import scenarios

# Set module-level logging
logger = logging.getLogger('daca')

def set_logging(debug=False):
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


def check_docker_version():
    # Use docker client instead
    logger.info("Checking docker version")
    #logger.exception("error") # prints nice stacktrace
    shutil.which("docker")
    subprocess.run(["which", "docker"], capture_output=True, encoding="UTF-8").stdout.strip()
    subprocess.run(["docker", "-v"], capture_output=True, encoding="UTF-8").stdout.strip()
    pass


if __name__ == '__main__':
    # Click - determine debug level
    set_logging()
    
    # daca.py --

    # daca.py --debug --scenario /path/to/scenario.yaml
    # daca.py --list-scenarios
    # daca.py --summarize --scenario-id 1

    # List available scenarios
    logger.debug("Listing out-of-the-box scenarios")
    scenarios = Path(r'scenarios').glob('*/*yaml*')
    scenario_list = [i for i in scenarios if i.is_file()]
    scenario_list.sort()
    for scenario in scenario_list:
        print(f"[{scenario_list.index(scenario)}]\t{scenario.name}")
        



    # Click - determine scenario
    #print(dns_tunnel.tralala())
    # Click - Interactive should be a flag?
    #chosen_scenario = "dns_tunnel"
    controller = VagrantController("asd")
    

    #for server in servers:
    #x = ScenarioRunner("asd")
    #x.run()
    logger.info("test log")