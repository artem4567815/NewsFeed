import boto3
import base64
import io
from PIL import Image
import os
import mimetypes
import random
import string
from datetime import datetime
from urllib.parse import urlparse


class MinioClient:
    def __init__(self, access_key: str, secret_key: str, endpoint: str, bucket: str, region: str = 'us-east-1'):
        self.__bucket = bucket
        self.client = boto3.client(
            's3',
            endpoint_url=f'http://{endpoint}',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=boto3.session.Config(signature_version='s3v4'),
            region_name=region
        )

    def _get_mime_type(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    def upload_base64(self, base64_string: str, directory: str):
        try:
            base64_data = base64_string.split(",")[1]
            image_data = base64.b64decode(base64_data)
            image = Image.open(io.BytesIO(image_data))

            characters = string.ascii_letters + string.digits
            random_name = ''.join(random.choices(characters, k=30))
            file_extension = base64_string.split(";")[0].split("/")[-1]
            partly_file_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
            file_name = f'{partly_file_name + "_" + random_name}.{file_extension}'

            os.makedirs("images", exist_ok=True)
            file_path = os.path.join("images", file_name)

            if file_extension == 'gif':
                image.save(file_path, save_all=True)
            else:
                image.save(file_path)

            content_type = self._get_mime_type(file_path)
            with open(file_path, "rb") as f:
                self.client.upload_fileobj(
                    f,
                    self.__bucket,
                    directory + "/" + file_name,
                    ExtraArgs={
                        "ContentType": content_type,
                        "ContentDisposition": "inline"
                    }
                )

            print(f"[OK] Uploaded {file_name} to {self.__bucket}")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Файл {file_path} был удалён.")
            else:
                print(f"Файл {file_path} не существует.")
            return directory + "/" + file_name

        except Exception as e:
            print(f"[ERROR] Failed to upload base64: {e}")
            return False

    def get_public_url(self, object_name: str) -> str:
        return f"https://{self.client.meta.endpoint_url.split('//')[1].split(":")[0]}/console/{self.__bucket}/{object_name}"


    def delete_file_by_url(self, url: str):
        parsed = urlparse(url)
        parts = parsed.path.lstrip("/").split("/", 2)
        if len(parts) < 3:
            raise ValueError("Invalid URL format for MinIO object.")

        bucket_name = parts[1]
        object_key = parts[2]

        try:
            self.client.delete_object(Bucket=bucket_name, Key=object_key)
            print(f'File "{object_key}" from bucket "{bucket_name}" deleted successfully.')
        except Exception as e:
            print(f'Error deleting file: {e}')
