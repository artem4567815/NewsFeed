from pydantic import BaseModel, Field, model_validator
from typing import Optional, List


class SubscribeRequest(BaseModel):
    tags: Optional[List[str]] = None
    authors: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_response(cls, values):
        if (values.tags is None and values.authors is None) or ((values.authors == [] and values.tags is None)
                                                                or (values.authors is None and values.tags ==[])):
            raise ValueError("tags and authors cannot be None")

        return values