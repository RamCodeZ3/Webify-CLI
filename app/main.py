import typer

from app.commands import converter_webp
from app.core.generate_favicon import FaviconGenerator

app = typer.Typer()
f = FaviconGenerator("/home/ramcodez3/Imágenes/imagen_test/logo.webp")
f.generate_all()

app.add_typer(converter_webp.app)

if __name__ == "__main__":
    app()
