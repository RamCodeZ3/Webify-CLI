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
    if path is None:
        typer.secho("specify the route", fg=typer.colors.RED)
        raise typer.Abort()

    if path == ".":
        path = str(Path.cwd())

    result = asyncio.run(_wc(path, delete_img))

    if result:
        typer.secho(
            f"A total of {result} images were converted to webp",
            fg=typer.colors.GREEN,
        )


async def _wc(path: str, delete_img: bool | None):
    return await convertor.convert_to_webp(path, delete_img)
