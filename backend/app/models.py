from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    url: str = Field(min_length=1, max_length=2048)


class ExtractResponse(BaseModel):
    platform: str
    url: str
    description: str
