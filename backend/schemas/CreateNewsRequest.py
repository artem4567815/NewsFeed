from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime
from zoneinfo import ZoneInfo

class CreateNewsRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    content: str = Field(..., min_length=10, max_length=300)
    short_content: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=100)
    start_date:  Optional[int] = None
    end_date: Optional[int] = None
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
