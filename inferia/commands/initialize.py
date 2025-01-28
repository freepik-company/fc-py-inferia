import click

from inferia.commands.scaffold_predict import scaffold_predict_classes
from inferia.core.config import (
    InferiaConfig,
    ConfigFile,
    FastAPIConfig,
    RouteConfig,
    ServerConfig,
    TrainingConfig,
)


def _init_with_default() -> ConfigFile:
    return ConfigFile.default()


def _init_prompted() -> ConfigFile:
    click.echo(
        "Please provide the following information to initialize the project configuration:"
    )
    name = click.prompt(
        "Project name", type=str, default="Sapientia per Inferentiam", show_default=True
    )
    description = click.prompt(
        "Project description", type=str, default=None, show_default=True
    )
    version = click.prompt(
        "Project version", type=str, default="1.0.0", show_default=True
    )

    click.echo("Nice! Now let's configure the FastAPI settings:")

    host = click.prompt("Host", type=str, default="0.0.0.0", show_default=True)
    port = click.prompt("Port", type=int, default=8000, show_default=True)
    debug = click.confirm(
        "Would you like to run the API server in DEBUG mode?",
        default=False,
        show_default=True,
    )
    access_log = click.confirm(
        "Would you like to enable access logs?", default=False, show_default=True
    )

    fastapi = FastAPIConfig(
        host=host,
        port=port,
        debug=debug,
        access_log=access_log,
    )

    click.echo("This starts to look like an amazing inference service!")

    routes = []

    if click.confirm(
        "Would you like to add a default route to the API?",
        default=True,
        show_default=True,
    ):
        routes.append(RouteConfig.default())

    server = ServerConfig(
        name=name,
        description=description,
        version=version,
        fastapi=fastapi,
        routes=routes,
    )

    click.echo("Almost there! Let's configure the training settings.")

    # todo add training settings, when defined

    training = TrainingConfig()

    click.echo("Great! We're all set.")

    inferia = InferiaConfig(
        server=server,
        training=training,
    )

    return ConfigFile(inferia=inferia)


@click.command()
@click.option(
    "-s",
    "--scaffold",
    is_flag=True,
    default=False,
    help="Create a scaffold predict class in predict.py",
)
@click.option(
    "-d",
    "--default",
    is_flag=True,
    default=False,
    help="Initialize with default values",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Force initialization, even if already initialized",
)
@click.pass_context
def init(
    ctx, scaffold: bool = False, default: bool = False, force: bool = False
) -> None:
    """Initialize the project configuration"""

    config_path = ctx.obj["config_path"]

    click.echo("Initializing...")

    if ConfigFile.exists(f"{config_path}/inferia.yaml") and not force:
        click.echo("Already initialized.")
        return

    if default:
        config = _init_with_default()
    else:
        config = _init_prompted()

    if scaffold:
        scaffold_predict_classes(config, force)

    config.save_to_file(f"{config_path}/inferia.yaml")
    click.echo("Initialized successfully.")
