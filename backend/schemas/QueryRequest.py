from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal, List
from datetime import datetime
from zoneinfo import ZoneInfo


class QueryRequest(BaseModel):
    type: Optional[str] = None
    limit: Optional[int] = Field(20, ge=0)
    offset: Optional[int] = Field(0, ge=0)
    start_date: Optional[int] = None
    end_date: Optional[int] = None
    tags: Optional[str] = None
    school: Optional[str] = None
    search: Optional[str] = None

    @model_validator(mode="after")
    def check_dates(cls, values):
        now_msk = datetime.now(ZoneInfo("Europe/Moscow"))
        now_ts = int(now_msk.timestamp())
        if values.start_date is not None:
            if values.start_date < now_ts:
                raise ValueError('start_date cannot be in the past')

        if  values.end_date is not None:
            if  values.end_date < now_ts:
                raise ValueError('end_date cannot be in the past')

        if values.start_date is not None and values.end_date is not None:
            if values.start_date > values.end_date:
                raise ValueError('start_date cannot be after end_date')

        return values


