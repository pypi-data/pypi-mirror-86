import logging

import click


@click.group()
@click.pass_context
@click.option('--verbose/--verbose-of', default=False)
def cli(ctx, verbose):
    print(ctx.obj)
    if verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


