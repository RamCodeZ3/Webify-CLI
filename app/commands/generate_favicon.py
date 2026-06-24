import asyncio
from pathlib import Path

import typer

from app.core.generate_favicon import FaviconGenerator
from app.utils.auto_complete import auto_complete_files

app = typer.Typer()


@app.command()
def favicon(
    path: str = typer.Argument(
        None,
        help="route where the images will be converted",
        autocompletion=auto_complete_files,
    ),
    name_app: str | None = typer.Option(
        None,
        "--name-app",
        "-name",
        help="website or app name",
    ),
    destination_path: str | None = typer.Option(
        None,
        "--destination",
        "-dest",
        help="favicon exit",
    ),
):

    if path is None:
        typer.secho("specify the file", fg=typer.colors.RED)
        raise typer.Abort()

    if destination_path is None:
        dest = Path(path)
        destination_path = str(dest.parent)

    asyncio.run(_favicon(path, name_app, destination_path))
    typer.echo("✅ All favicons were created correctly")


async def _favicon(path: str, name_app: str | None, destination: str | None):
    favicon = FaviconGenerator(path, name_app, destination)
    await favicon.generate_all()
