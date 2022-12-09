from fastapi import APIRouter
from util import tokens
from models import token as models
from models import response


router = APIRouter()


@router.post("/tokens/", response_model=response.TokenCreated, tags=["tokens"])
async def create_token_endpoint(token: models.Token):
    """
    Create a token based on an existing set of clientId and secret.
    And this path operation will:

    * Create a token using existing credentials.
    * Returns the token to be used by the client.
    """
    created = tokens.create_token(identifier=token.client_id[0], secret=token.secret)
    return {"authorization": f"Bearer {created}"}
