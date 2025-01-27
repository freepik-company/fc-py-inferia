import os

import click

from inferia import Application
from inferia.core.config import ConfigFile


@click.command()
@click.pass_obj
def run(ctx):
    """Run cogito app"""
    config_path = ctx.get("config_path")
    absolute_path = os.path.abspath(config_path)
    click.echo(f"Running '{absolute_path}' cogito application...")
    # change cwd to config_path
    os.chdir(absolute_path)
    if ConfigFile.exists("cogito.yaml"):
        click.echo("Cogito application is initialized.")

    app = Application(config_file_path=absolute_path)
    app.run()
