from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class PatchUserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    surname: Optional[str] = Field(None, min_length=1, max_length=120)
    building: Optional[str] = Field(None, min_length=1, max_length=100)
    login: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None

    class Config:
        extra = "forbid"

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

    @field_validator("building")
    @classmethod
    def validate_building(cls, value):
        value = value.strip()
        if re.fullmatch(r"-?\d+", value):
            if int(value) < 0:
                raise ValueError("Номер корпуса не может быть отрицательным")
        return value