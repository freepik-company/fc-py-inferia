import click
import tomli
from pathlib import Path


@click.command()
def version():
    """Muestra la versión actual de Cogito."""
    try:
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomli.load(f)
            version = pyproject_data["project"]["version"]
            click.echo(f"Cogito version {version}")
    except Exception as e:
        click.echo(f"Error reading version: {str(e)}", err=True)
        raise click.Abort()
