import typer

from app.commands import converter_webp

app = typer.Typer()

app.add_typer(converter_webp.app)

if __name__ == "__main__":
    app()
