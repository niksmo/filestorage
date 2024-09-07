from pydantic import BaseModel as BaseSchema, Field


class ServiceActiveTime(BaseSchema):
    db: float = Field(examples=[2.32])
