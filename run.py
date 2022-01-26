#!/usr/bin/env python3
from curses.ascii import SO
import logging
import subprocess
import shutil

from daca.daca import *

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
    

def test():
    logger.info("Running test()")
    logger.exception("help")
    print("test")


def check_docker_version():
    shutil.which("docker")
    subprocess.run(["which", "docker"], capture_output=True, encoding="UTF-8").stdout.strip()
    subprocess.run(["docker", "-v"], capture_output=True, encoding="UTF-8").stdout.strip()
    pass

def check_vagrant_version():
    pass


if __name__ == '__main__':
    set_logging() # pass args.debug to it later
    test()
    x = Something()
    print(x.x)