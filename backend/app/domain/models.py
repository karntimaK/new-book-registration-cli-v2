from pydantic import BaseModel, Field, field_validator
from uuid import uuid4

class Book(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    author: str
    isbn: str

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit():
            raise ValueError("ISBN ต้องเป็นตัวเลขเท่านั้น")
        if len(v) != 13:
            raise ValueError("ISBN ต้องมี 13 หลัก")
        return v


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit():
            raise ValueError("ISBN ต้องเป็นตัวเลขเท่านั้น")
        if len(v) != 13:
            raise ValueError("ISBN ต้องมี 13 หลัก")
        return v


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v.isdigit():
            raise ValueError("ISBN ต้องเป็นตัวเลขเท่านั้น")
        if len(v) != 13:
            raise ValueError("ISBN ต้องมี 13 หลัก")
        return v
