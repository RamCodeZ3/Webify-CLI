import typer

from commands import converter_webp

app = typer.Typer()

app.add_typer(converter_webp.app, name="webify")

if __name__ == "__main__":
    app()
