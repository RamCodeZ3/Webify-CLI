import os

from PIL import Image

from app.utils.report import report_outcome

extensions = (".jpeg", ".png", ".jpg")


class ConvertToWebp:
    async def convert_to_webp(self, path: str, delete_img: bool | None):
        if os.path.isfile(path):
            self._convert_to_webp(path, delete_img)

        else:
            files = [f for f in os.listdir(path) if f.endswith(extensions)]
            if len(files) == 0:
                print("No images were found in the specified directory")

            else:
                for file in os.listdir(path):
                    full_route = os.path.join(path, file)
                    name, extension = os.path.splitext(full_route)
                    if os.path.isfile(full_route) and extension in extensions:
                        self._convert_to_webp(full_route, delete_img)
                return len(files)

    @report_outcome(
        success_message="It was successfully converted to",
        error_message="There was an error",
    )
    def _convert_to_webp(self, full_route, delete_img: bool | None):
        name, extension = os.path.splitext(full_route)
        image = Image.open(full_route)
        image = image.convert("RGB")
        image_path = f"{name}.webp"
        image.save(image_path, "webp")

        if not delete_img:
            os.remove(full_route)

        return f"{os.path.basename(name)}.webp"


convertor = ConvertToWebp()
