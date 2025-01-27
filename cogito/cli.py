import click

from cogito.commands.initialize import init
from cogito.commands.scaffold_predict import scaffold


@click.group()
@click.option(
    "-c",
    "--config-path",
    type=str,
    default=".",
    help="The path to the configuration file",
)
@click.pass_context
def cli(ctx, config_path: str = ".") -> None:
    """
    Cogito CLI
    """
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path


cli.add_command(init)
cli.add_command(scaffold)

if __name__ == "__main__":
    cli(obj={})
