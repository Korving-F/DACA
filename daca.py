#!/usr/bin/env python3
import logging
import subprocess
import shutil
import docker

# Local Modules
from daca import *
from daca.vagrantcontroller import VagrantController
from daca.scenariorunner import ScenarioRunner

# Set module-level logging
logger = logging.getLogger(__name__)

def set_logging(debug=False):
    """
    Set logging parameters.

    Keyword arguments:
    debug -- enable debug level logging (default False)
    """
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [ %(filename)s:%(lineno)s %(funcName)s %(levelname)s ] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def check_docker_version():
    logger.info("Checking docker version")
    #logger.exception("error") # prints nice stacktrace
    shutil.which("docker")
    subprocess.run(["which", "docker"], capture_output=True, encoding="UTF-8").stdout.strip()
    subprocess.run(["docker", "-v"], capture_output=True, encoding="UTF-8").stdout.strip()
    pass




if __name__ == '__main__':
    


    # Click - determine debug level
    set_logging()

    # Click - determine scenario
    #print(dns_tunnel.tralala())
    # Click - Interactive should be a flag?
    #chosen_scenario = "dns_tunnel"
    #controller = VagrantController(chosen_scenario)
    

    #for server in servers:
    x = ScenarioRunner("asd")
    x.run()
