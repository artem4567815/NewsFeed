from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, List
from datetime import datetime
from zoneinfo import ZoneInfo
import re

class PatchPostRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    short_content: Optional[str] = Field(None, min_length=1)
    start_date:  Optional[int] = Field(None, ge=0)
    end_date: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        extra = "forbid"

    @model_validator(mode="after")
    def check_dates(cls, values):
        now_msk = datetime.now(ZoneInfo("Europe/Moscow"))
        now_ts = int(now_msk.timestamp())
        if values.start_date is not None:
            if values.start_date < now_ts:
                raise ValueError('start_date cannot be in the past')

        if values.end_date is not None:
            if values.end_date < now_ts:
                raise ValueError('end_date cannot be in the past')

        if values.start_date is not None and values.end_date is not None:
            if values.start_date > values.end_date:
                raise ValueError('start_date cannot be after end_date')

        return values

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value):
        if value is not None:
            if value == "" or value == " ":
                return None

            if not value.startswith("data:image/"):
                raise ValueError("Некорректный формат изображения")

            base64_pattern = r"^data:image\/[a-zA-Z]*;base64,[A-Za-z0-9+/=]*$"
            if not re.match(base64_pattern, value):
                raise ValueError("Некорректный формат base64 для изображения")

        return value
