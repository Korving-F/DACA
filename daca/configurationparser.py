from jinja2 import Environment, PackageLoader, select_autoescape

class ConfigurationParser:
    def __init__(self) -> None:
        self._env = Environment(loader=PackageLoader('daca'),
                                autoescape=select_autoescape())