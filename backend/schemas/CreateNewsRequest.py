from pydantic import BaseModel, Field


class CreateNewsRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    content: str = Field(..., min_length=10, max_length=300)
    short_content: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=100)
    start_date: int = Field(...)
    end_date: int = Field(...)
    post_img: str = Field(...)
    post_img_detail: str = Field(...)
