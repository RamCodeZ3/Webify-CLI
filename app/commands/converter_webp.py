import asyncio
from pathlib import Path

import typer

from core.converter import convert_to_webp

app = typer.Typer()


@app.command()
def wc(
    path: str | None = typer.Argument(
        None, help="route where the images will be converted"
    ),
    delete_img: bool = typer.Option(
        False,
        "--not-delete",
        "-f",
        help="disable the deletion of original images",
    ),
):

    if path is None:
        path = str(Path.cwd())

    asyncio.run(_wc(path, delete_img))
    typer.echo("✅ All images were converted correctly")


async def _wc(path: str, delete_img: bool | None):
    await convert_to_webp(path, delete_img)
