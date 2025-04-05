import base64
import os
import random
import string
from config import UPLOADFLOADER
import io
from PIL import Image
from flask import url_for


def save_base64_image(base64_string):
    if not base64_string.startswith("data:image/"):
        raise ValueError("Некорректный формат base64 (ожидается data:image/...)")

    base64_data = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    os.makedirs(UPLOADFLOADER, exist_ok=True)
    file_extension = base64_string.split(";")[0].split("/")[-1]
    characters = string.ascii_letters + string.digits
    filename = ''.join(random.choices(characters, k=30))

    file_path = os.path.join(UPLOADFLOADER, f"{filename}.{file_extension}")

    if file_extension == 'gif':
        image.save(file_path, save_all=True)
    else:
        image.save(file_path)

    path = url_for('serve_image', filename=f"{filename}.{file_extension}", _external=True)

    return str(path)
