import typer
import asyncio

from core.converter import convert_to_webp

app = typer.Typer()

@app.command()
def wc(path: str):
    asyncio.run(_wc(path))
    typer.echo("✅ All images were converted correctly")


async def _wc(path: str):
    await convert_to_webp(path)
