"""Contains the CLI commands."""

import click
import logging
from pathlib import Path
from importlib import metadata
from . import pkgname
from .hello import Hello, HelloError

logger = logging.getLogger(__name__)


# click entrypoint
@click.group()
@click.option('-c', '--config', type=click.Path(),
              default=Path(f'~/.{pkgname}.yml').expanduser(),
              help='Specify a configuration file.')
@click.option('-v', '--verbose', count=True, help='Set verbosity level.')
@click.option('-l', '--log', type=click.Path(), help='Path to an output log file')
@click.version_option(metadata.version(pkgname))
@click.pass_context
def main(ctx, log, verbose, config):
    """Scaffold a python3 CLI project."""
    # set log level with format
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    fmt = '[%(levelname)s] %(message)s'

    if verbose == 1:
        logger.setLevel(logging.INFO)
        fmt = '[%(levelname)s] %(name)s: %(message)s'

    elif verbose == 2:
        logger.setLevel(logging.DEBUG)
        fmt = '[%(levelname)s] %(module)s: %(message)s'

    handler = logging.StreamHandler()
    if log:
        # log in file with timeline
        fmt = '%(asctime)s ' + fmt
        handler = logging.FileHandler(log)

    # configure root logger
    formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%dT%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Run the program
    try:
        # load main controller in context
        ctx.obj = Hello(config)

    except HelloError as e:
        click.echo(str(e))


@main.command()
@click.pass_obj
def speak(hello):
    """Say something to the world."""
    try:
        click.echo(hello.msg)
    except HelloError as e:
        click.echo(e)


@main.command()
@click.pass_obj
def print(hello):
    """Print some data from packages."""
    try:
        click.echo(hello.get_data())
    except HelloError as e:
        click.echo(e)
