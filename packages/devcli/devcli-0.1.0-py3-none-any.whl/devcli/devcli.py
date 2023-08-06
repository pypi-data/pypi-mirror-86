import importlib
import logging
import pkgutil

import click

from devcli.context import DevCliContext



@click.group()
@click.pass_context
@click.option('--verbose/--verbose-of', default=False)
def cli(ctx, verbose):
    print(ctx.obj)
    if verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


