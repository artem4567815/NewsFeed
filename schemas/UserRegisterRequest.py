from pydantic import BaseModel, Field, field_validator

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=120)
    school: str = Field(..., min_length=1, max_length=100)
    building: str = Field(..., min_length=1, max_length=100)
    login: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=60)


    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not (8 <= len(value) <= 60 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value)):
            raise ValueError('Password incorrect')
        return value