### System modules ###
import shutil
import subprocess
import docker

### Local modules ###
from .controller import Controller

### Setup logging ###
import logging
logger = logging.getLogger('daca')

class DockerController(Controller):
    def __init__(self) -> None:
        pass

    def check_controller_version(self):
        # Use docker client instead
        logger.info("Checking docker version")
        #logger.exception("error") # prints nice stacktrace
        shutil.which("docker")
        subprocess.run(["which", "docker"], capture_output=True, encoding="UTF-8").stdout.strip()
        subprocess.run(["docker", "-v"], capture_output=True, encoding="UTF-8").stdout.strip()
        pass