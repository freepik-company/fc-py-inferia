import click

from cogito.commands.initialize import initialize


@click.group()
def cli():
    """
Cogito CLI
    """
    pass

cli.add_command(initialize)