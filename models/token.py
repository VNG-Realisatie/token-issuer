from pydantic import BaseModel


class Token(BaseModel):
    client_id: list[str]
    secret: str
