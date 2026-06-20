import base64
import json
import os
import struct

from PIL import Image

from app.core.contants import FAVICON_TYPES
from app.utils.report import report_outcome


class FaviconGenerator:
    def __init__(
        self,
        source_path: str,
        name_app: str | None,
        destination_path: str | None,
    ) -> None:
        self.source_path = source_path
        self.name_app = name_app or "MyWebSite"

        if not os.path.isfile(self.source_path):
            raise FileNotFoundError(
                f"Source image not found: {self.source_path}"
            )

        base_dest = destination_path or os.path.dirname(self.source_path)
        self.output_dir = os.path.join(base_dest, "favicon")

        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_all(self) -> dict[str, str | Exception]:
        results: dict[str, str | Exception] = {}

        for favicon_type in FAVICON_TYPES:
            result = self._generate(favicon_type)
            results[favicon_type["prefix"]] = result

        self._generate_webmanifest()
        await self._generate_code()

        return results

    @report_outcome(
        success_message="The file was created successfully",
        error_message="There was an error creating the file",
    )
    def _generate(self, favicon_type: dict) -> str:
        filename = f"{favicon_type['prefix']}.{favicon_type['image_fmt']}"
        dest = os.path.join(str(self.output_dir), filename)

        if favicon_type["image_fmt"] == "svg":
            self._copy_as_svg(dest)
            return filename

        if favicon_type["image_fmt"] == "ico":
            self._generate_ico(dest)
            return filename

        with Image.open(self.source_path) as img:
            img_copy = img.convert("RGBA")
            img_copy = img_copy.resize(
                favicon_type["dimensions"], Image.Resampling.LANCZOS
            )
            save_kwargs = self._build_save_kwargs(favicon_type)
            img_copy.save(dest, **save_kwargs)

        return filename

    @report_outcome(success=False)
    def _generate_ico(self, dest: str) -> str:
        ico_sizes = [(48, 48), (32, 32), (16, 16)]
        with Image.open(self.source_path) as img:
            img = img.convert("RGBA")
            self._write_ico_bmp(img, dest, ico_sizes)
        return dest

    @staticmethod
    def _write_ico_bmp(
        source_img: Image.Image, dest: str, sizes: list[tuple[int, int]]
    ) -> None:

        entries = []
        images_data = []

        for w, h in sizes:
            resized = source_img.resize((w, h), Image.Resampling.LANCZOS)
            pixels = resized.load()

            raw = bytearray()
            for y in reversed(range(h)):
                for x in range(w):
                    r, g, b, a = pixels[x, y]
                    raw += struct.pack("<BBBB", b, g, r, a)

            bmp_header = struct.pack(
                "<IiiHHIIiiII",
                40,  # header size
                w,  # width
                h * 2,  # height x2
                1,  # plans
                32,  # bits by pixel
                0,  # without compression (BI_RGB)
                len(raw),  # image size in bytes
                0,
                0,
                0,
                0,
            )

            and_mask_row_bytes = ((w + 31) // 32) * 4
            and_mask = bytes(and_mask_row_bytes * h)

            img_bytes = bmp_header + bytes(raw) + and_mask
            images_data.append(img_bytes)
            entries.append(
                {
                    "width": w if w < 256 else 0,
                    "height": h if h < 256 else 0,
                    "size": len(img_bytes),
                }
            )

        out = struct.pack("<HHH", 0, 1, len(sizes))

        offset = 6 + len(sizes) * 16
        for entry, img_bytes in zip(entries, images_data):
            out += struct.pack(
                "<BBBBHHII",
                entry["width"],
                entry["height"],
                0,  # colors
                0,  # reserved
                1,  # planes
                32,  # bpp
                entry["size"],
                offset,
            )
            offset += len(img_bytes)

        for img_bytes in images_data:
            out += img_bytes

        with open(dest, "wb") as f:
            f.write(out)

    def _build_save_kwargs(self, favicon_type: dict) -> dict:
        fmt = favicon_type["image_fmt"].upper()
        kwargs: dict = {"format": fmt}

        if fmt == "PNG":
            kwargs["optimize"] = True

        elif fmt == "ICO":
            kwargs["sizes"] = [favicon_type["dimensions"]]

        return kwargs

    def _copy_as_svg(self, dest: str) -> None:
        with Image.open(self.source_path) as img:
            img = img.convert("RGBA")
            w, h = img.size

            from io import BytesIO

            buf = BytesIO()
            img.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")

        svg_content = (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<image width="{w}" height="{h}" '
            f'href="data:image/png;base64,{b64}"/></svg>'
        )

        with open(dest, "w", encoding="utf-8") as f:
            f.write(svg_content)

    async def _generate_code(self):
        print(f"""
        [HTML code]
        <link rel="icon" type="image/png" href="/favicon/favicon-96x96.png" sizes="96x96" />
        <link rel="icon" type="image/svg+xml" href="/favicon/favicon.svg" />
        <link rel="shortcut icon" href="/favicon/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/favicon/apple-touch-icon.png" />
        <meta name="apple-mobile-web-app-title" content="{self.name_app}" />
        <link rel="manifest" href="/favicon/site.webmanifest" />
        """)

    @report_outcome(
        success_message="The file was created successfully",
        error_message="There was an error creating the file",
    )
    def _generate_webmanifest(self) -> str:
        manifest_data = {
            "name": f"{self.name_app}",
            "short_name": f"{self.name_app}",
            "icons": [
                {
                    "src": "/favicon/web-app-manifest-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "maskable",
                },
                {
                    "src": "/favicon/web-app-manifest-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "maskable",
                },
            ],
            "theme_color": "#ffffff",
            "background_color": "#ffffff",
            "display": "standalone",
        }

        with open(
            f"{self.output_dir}/site.webmanifest", "w", encoding="utf-8"
        ) as f:
            json.dump(manifest_data, f, indent=4, ensure_ascii=False)

        return "site.webmanifest"
