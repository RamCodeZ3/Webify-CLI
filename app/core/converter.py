import os

from PIL import Image

extensions = [".jpeg", ".png", ".jpg"]


async def convert_to_webp(path: str, delete_img: bool | None):
    try:
        for file in os.listdir(path):
            name, extension = os.path.splitext(file)
            full_route = os.path.join(path, file)

            if os.path.isfile(full_route) and extension in extensions:
                image = Image.open(full_route)
                image = image.convert("RGB")

                image_path = os.path.join(path, f"{name}.webp")
                image.save(image_path, "webp")
                print(f"[✅]{name}{extension} -> {name}.webp")

                if not delete_img:
                    os.remove(full_route)

    except Exception as e:
        raise ValueError("[❌]There was an error: ", e)
