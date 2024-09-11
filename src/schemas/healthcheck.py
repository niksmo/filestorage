from pydantic import BaseModel as BaseSchema, Field


class ServiceActiveTime(BaseSchema):
    db: int = Field(examples=[1753])
    cache: int = Field(examples=[3472])
