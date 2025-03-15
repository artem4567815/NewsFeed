from pydantic import BaseModel, Field


class CreateNewsRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    full_description: str = Field(..., min_length=10, max_length=300)
    short_description: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=100)
    input: str = Field(..., min_length=1, max_length=300)
    dataURL: str = Field(...)
