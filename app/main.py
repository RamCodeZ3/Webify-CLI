import typer

from app.commands import converter_webp
from app.commands import generate_favicon


app = typer.Typer()

app.add_typer(converter_webp.app)
app.add_typer(generate_favicon.app)

if __name__ == "__main__":
    app()
