from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from zoneinfo import ZoneInfo
import re
from urllib.parse import urlparse


class CreateNewsRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=10)
    short_content: str = Field(..., min_length=1)
    type: Literal["news", "wallpapers"] = Field(...)
    start_date:  Optional[int] = Field(None, ge=0)
    end_date: Optional[int] = Field(None, ge=0)
    post_img: Optional[str] = None
    post_img_detail: Optional[str] = None
    tags: Optional[List[str]] = None

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

    @field_validator("post_img")
    @classmethod
    def validate_post_img(cls, value):
        if value is None or value.strip() == "":
            return None

        if value.startswith("data:image/"):
            base64_pattern = r"^data:image\/[a-zA-Z]+;base64,[A-Za-z0-9+/=\s]+$"
            if not re.match(base64_pattern, value):
                raise ValueError("Некорректный формат base64 изображения")
            return value

        parsed = urlparse(value)
        if parsed.scheme in ('http', 'https') and bool(parsed.netloc):
            return value


        raise ValueError("post_img должен быть либо base64-строкой, либо URL-ссылкой")