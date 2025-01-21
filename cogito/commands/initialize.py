import click

from cogito.core.config import ConfigFile
from cogito.core.exceptions import ConfigFileNotFoundError


@click.command()
def initialize(config_path: str = "."):
    """ Initialize the project configuration """
    click.echo("Initializing...")

    try:
        config = ConfigFile.load_from_file(f"{config_path}/cogito.yaml")
        click.echo("Already initialized.")
    except ConfigFileNotFoundError:
        config = ConfigFile.default()
        config.save_to_file(f"{config_path}/cogito.yaml")
        click.echo("Initialized successfully.")

