from pydantic import BaseModel as BaseSchema


class TokenBase(BaseSchema):
    token_type: str


class Token(TokenBase):
    access_token: str
