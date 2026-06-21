import asyncio
from pathlib import Path

import typer

from app.core.converter import convertor
from app.utils.auto_complete import auto_complete_files

app = typer.Typer()


@app.command()
def wc(
    path: str | None = typer.Argument(
        None,
        help="route where the images will be converted",
        autocompletion=auto_complete_files,
    ),
    delete_img: bool = typer.Option(
        False,
        "--not-delete",
        "-f",
        help="disable the deletion of original images",
    ),
):

    if path == ".":
        path = str(Path.cwd())

    asyncio.run(_wc(path, delete_img))
    typer.echo("✅ All images were converted correctly")


async def _wc(path: str, delete_img: bool | None):
    await convertor.convert_to_webp(path, delete_img)
