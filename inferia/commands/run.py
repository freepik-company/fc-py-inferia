import os
import sys

import click

from inferia import Application
from inferia.core.config import ConfigFile


@click.command()
@click.pass_obj
def run(ctx):
    """Run cogito app"""
    config_path = ctx.get("config_path")
    absolute_path = os.path.abspath(config_path)
    click.echo(f"Running '{absolute_path}' inferia application...")
    # change cwd to config_path
    os.chdir(absolute_path)
    if not os.path.exists(absolute_path):
        click.echo(f"Path '{absolute_path}' does not exist.")
        exit(1)
    else:
        # Add the config_path to the sys.path
        sys.path.insert(0, absolute_path)
        app = Application(config_file_path=absolute_path)
        app.run()
