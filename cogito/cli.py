import click

from cogito.commands.initialize import init


@click.group()
def cli():
    """
Cogito CLI
    """
    pass

cli.add_command(init)


if __name__ == "__main__":
    cli()