import sys
from typing import Any

import click

from .. import runner


@click.command()
@click.option('--build', '-b', is_flag=True, help='Flag to build the lambda(s)')
@click.option('--serve', '-s', is_flag=True, help='Flag to serve the lambda(s)')
@click.option('--config', '-c', default=None, help=(
    'The location of an optional configuration file to use, if not the default'
))
@click.option('--setup', is_flag=True, help=(
    'Create or overwrite the localambda configuration file'
))
def entry(build, serve, config, setup):
    """Input into localambda that determines whether or not to build or to
    serve the lambda. If no input is provided then the lambda is both 
    built and served.
    """
    if setup:
        runner.setup()
    else:
        cr = runner.CommandRunner(config=config)
        cr.add_step('build', build)
        cr.add_step('serve', serve)
        cr.run()