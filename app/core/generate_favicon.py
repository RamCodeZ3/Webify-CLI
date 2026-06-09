import os
import shutil

from PIL import Image

from app.core.contants import FAVICON_TYPES


class FaviconGenerator:

    def __init__(self, source_path: str) -> None:
        self.source_path = source_path

        if not os.path.isfile(self.source_path):
            raise FileNotFoundError(f"Source image not found: {self.source_path}")

        self.output_dir = os.path.dirname(self.source_path)

    def generate_all(self) -> dict[str, str | Exception]:
        results: dict[str, str | Exception] = {}

        for favicon_type in FAVICON_TYPES:
            result = self._generate(favicon_type)
            results[favicon_type["prefix"]] = result
            if isinstance(result, Exception):
                print(f"[ERROR] {favicon_type['prefix']}: {result}")
            else:
                print(f"[OK]    {favicon_type['prefix']}: {result}")

        return results

    def _generate(self, favicon_type: dict) -> str | Exception:
        try:
            filename = f"{favicon_type['prefix']}.{favicon_type['image_fmt']}"
            dest = os.path.join(self.output_dir, filename)

            if favicon_type["image_fmt"] == "svg":
                self._copy_as_svg(dest)
                return dest

            with Image.open(self.source_path) as img:
                # Always convert to RGBA — required for ICO transparency and safe for PNG
                img_copy = img.convert("RGBA")
                img_copy = img_copy.resize(favicon_type["dimensions"], Image.Resampling.LANCZOS)

                save_kwargs = self._build_save_kwargs(favicon_type)
                img_copy.save(dest, **save_kwargs)

            return dest

        except Exception as exc:  # noqa: BLE001
            return exc

    def _build_save_kwargs(self, favicon_type: dict) -> dict:
        fmt = favicon_type["image_fmt"].upper()
        kwargs: dict = {"format": fmt}

        if fmt == "PNG":
            kwargs["optimize"] = True

        return kwargs

    def _copy_as_svg(self, dest: str) -> None:
        filename, extension = os.path.splitext(self.source_path)

        if extension == ".svg":
            shutil.copy2(self.source_path, dest)
        else:
            raise RuntimeError(
                f"Source {filename} is not an SVG file; "
                "favicon.svg cannot be generated automatically with Pillow."
            )
