import logging
import os
import pathlib
import sys

import click
from xcraft.providers.lxd import LXDProvider

from mycraft.lifecycle_providers.executed import MycraftExecutedProvider
from mycraft.lifecycle_providers.host import MycraftHostProvider


@click.group()
@click.option("--debug", is_flag=True, default=False)
@click.option("--shell", is_flag=True, default=False)
@click.option(
    "--provider",
    type=click.Choice(["host", "lxd"]),
    default="host",
    envvar="MYCRAFT_PROVIDER",
)
@click.option("--output", type=str, default=os.path.join(os.getcwd(), "artifacts"))
@click.pass_context
def main(ctx, debug: bool, shell: bool, provider: str, output: str) -> int:
    ctx.ensure_object(dict)

    logging.basicConfig(level=logging.DEBUG)

    host_project_dir = pathlib.Path(os.getcwd())
    output_path = pathlib.Path(output)

    if provider == "host":
        ctx.obj["provider"] = MycraftHostProvider(artifacts_dir=output_path)
    elif provider == "lxd":
        env_provider = LXDProvider(instance_name="mycraft-project")
        env_provider.setup()
        ctx.obj["provider"] = MycraftExecutedProvider(
            env_provider=env_provider,
            host_artifacts_dir=output_path,
            host_project_dir=host_project_dir,
        )
    else:
        raise RuntimeError("unknown provider")

    ctx.obj["provider"].setup()

    return 0


@main.command("catalog")
@click.pass_context
def catalog(ctx) -> int:
    ctx.obj["provider"].catalog()
    return 0


@main.command("pull")
@click.argument("parts", nargs=-1, metavar="<part>...", required=False)
@click.pass_context
def pull(ctx, parts) -> int:
    ctx.obj["provider"].pull(parts=parts)
    return 0


@main.command("craft")
@click.pass_context
def craft(ctx) -> int:
    crafted = ctx.obj["provider"].craft()

    for c in crafted:
        click.echo(f"Crafted: {crafted}")

    return 0


@main.command("clean")
@click.argument("parts", nargs=-1, metavar="<part>...", required=False)
@click.pass_context
def clean(ctx, parts) -> int:
    if parts:
        ctx.obj["provider"].clean_parts(parts=parts)
    else:
        ctx.obj["provider"].clean()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
