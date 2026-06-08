from PIL import Image
import os


async def convert_to_webp(path: str):

    for file in os.listdir(path):
        name, extension = os.path.splitext(file)
        full_route = os.path.join(path, file)

        if os.path.isfile(full_route) and extension == '.jpeg' or extension == '.png':

            image = Image.open(full_route)
            image = image.convert('RGB')

            image_path = os.path.join(path, f"{name}.webp")
            image.save(image_path,"webp")
            print(f"{name}{extension} -> {name}.webp")

