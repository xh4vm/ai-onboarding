import orjson
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import datetime


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True


class UUIDMixin(BaseModel):
    id: UUID | None = Field(default_factory=lambda: uuid4())


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
