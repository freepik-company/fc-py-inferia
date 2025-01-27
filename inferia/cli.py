import click

from inferia.commands.initialize import init
from inferia.commands.scaffold_predict import scaffold
from inferia.commands.run import run


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
    Inferia CLI
    """
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path


cli.add_command(init)
cli.add_command(scaffold)
cli.add_command(run)


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
