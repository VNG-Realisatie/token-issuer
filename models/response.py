from pydantic import BaseModel


class Health(BaseModel):
    health: bool


class Propagation(BaseModel):
    endpoint: str
    success: bool
    client_id: str


class TokenPropagated(BaseModel):
    propagated: list[Propagation]
    authorization: str


class TokenCreated(BaseModel):
    authorization: str


class BadRequest(BaseModel):
    message: dict
