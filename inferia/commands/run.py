import os
import sys

import click

from inferia import Application


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
        click.echo(f"Error: Path '{absolute_path}' does not exist.", err=True, color=True)
        exit(1)

    try:
        sys.path.insert(0, absolute_path)
        app = Application(config_file_path=absolute_path)
        app.run()
    except Exception as e:
        click.echo(f"Error: {e}", err=True, color=True)
        exit(1)
