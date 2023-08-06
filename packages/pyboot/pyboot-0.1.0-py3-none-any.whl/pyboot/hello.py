"""Main controller module."""

import logging
import yaml
from importlib import resources
from . import pkgname

logger = logging.getLogger(__name__)


class HelloError(Exception):
    """Basic exception raised by the program."""


class Hello(object):
    """Example of class."""

    def __init__(self, config_file=None):
        """
        Initiate the controller.

        :param config_file: If given, the path to the configuration file
        """
        self.msg = 'Hello world!'
        self.config_file = config_file
        self._config = None

    @property
    def config(self):
        """Load configuration from file."""
        try:
            if not self._config:
                self._config = yaml.safe_load(open(self.config_file, 'r'))

        except FileNotFoundError:
            raise HelloError(f'No config file found at {self.config_file}')

        except yaml.YAMLError as e:
            logger.debug(e)
            raise HelloError(f'Error loading configuration from {self.config_file}')

    @config.setter
    def config(self, value):
        """Set a dict has current configuration."""
        self._config = value

    def get_data(self):
        """Display content of the text file in the root package."""
        return resources.read_text(pkgname, 'text')
        # with resources.path(pkgname, 'samples') as _dir:
        #    return [f.name for f in _dir.rglob('*.md')
