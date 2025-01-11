import base64
import os
import random
import string


def save_file(image):
    SAVE_FOLDER = "static/images"

    header, encoded = image.split(',', 1)
    image_data = base64.b64decode(encoded)

    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    if not os.path.exists(os.path.join(SAVE_FOLDER, f"{random_name}.png")):
        file_path = os.path.join(SAVE_FOLDER, f"{random_name}.png")
    else:
        file_path = os.path.join(SAVE_FOLDER, f"{random_name}_1.png")

    with open(file_path, 'wb') as f:
        f.write(image_data)

    return f"images/{random_name}.png"
