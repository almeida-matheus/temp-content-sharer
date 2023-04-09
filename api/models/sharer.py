from pydantic import BaseModel, Field
from typing import Optional

class TextRequest(BaseModel):
    text: str
    name: Optional[str] = Field('')
    extension: Optional[str] = Field('.txt')
    expiration: Optional[int] = Field(86400)

class FileGetRequest(BaseModel):
    name: str
    expiration: Optional[int] = Field(86400)

class FilePostResponse(BaseModel):
    url: str
    fields: dict

class SharerResponse(BaseModel):
    temporary_url: str