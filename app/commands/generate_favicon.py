import asyncio
from pathlib import Path
import typer
from app.core.generate_favicon import FaviconGenerator

app = typer.Typer()


def auto_complete_files(incomplete: str):
    partial_path = Path(incomplete) if incomplete else Path(".")

    if partial_path.is_dir():
        base_dir = partial_path
        prefix = ""
    
    else:
        base_dir = partial_path.parent if str(partial_path.parent) != "" else Path(".")
        prefix = partial_path.name

    try:
        entries = list(base_dir.iterdir())
    
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return []

    matches = []
    for entry in entries:
        if entry.name.startswith(prefix):
            candidate = str(entry) + ("/" if entry.is_dir() else "")
            matches.append(candidate)

    return matches


@app.command()
def favicon(
    path: str = typer.Argument(
        ...,
        help="route where the images will be converted",
        autocompletion=auto_complete_files,
    ),
    name_app: str | None = typer.Option(
        None,
        "--name-app",
        "-name",
        help="",
    ),
    destination_path: str | None = typer.Option(
        None,
        "--destination",
        "-dest",
        help="",
    ),
):

    if destination_path is None:
        dest = Path(path)
        destination_path = str(dest.parent)

    asyncio.run(_favicon(path, name_app, destination_path))
    typer.echo("✅ All favicons were created correctly")


async def _favicon(path: str, name_app: str | None, destination: str | None):
    favicon = FaviconGenerator(path, name_app, destination)
    await favicon.generate_all()
