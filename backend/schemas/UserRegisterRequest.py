from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=120)
    school: str = Field(..., min_length=1, max_length=100)
    building: str = Field(..., min_length=1, max_length=100)
    login: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=60)
    avatar_url: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not (8 <= len(value) <= 60 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value)):
            raise ValueError('Password incorrect')
        return value

    @field_validator("avatar_url")
    @classmethod
    def validate_avatar_url(cls, value):
        if value is not None:
            if  value == "" or value == " ":
                return None

            if not value.startswith("data:image/"):
                raise ValueError("Некорректный формат изображения")

            base64_pattern = r"^data:image\/[a-zA-Z]*;base64,[A-Za-z0-9+/=]*$"
            if not re.match(base64_pattern, value):
                raise ValueError("Некорректный формат base64 для изображения")

        return value

    @field_validator("school")
    @classmethod
    def validate_school(cls, value):
        value = value.strip()
        if re.fullmatch(r"-?\d+", value):
            if int(value) < 0:
                raise ValueError("Номер школы не может быть отрицательным")
        return value

    @field_validator("building")
    @classmethod
    def validate_building(cls, value):
        value = value.strip()
        if re.fullmatch(r"-?\d+", value):
            if int(value) < 0:
                raise ValueError("Номер корпуса не может быть отрицательным")
        return value
