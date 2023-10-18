from fastapi import APIRouter, Request

from models import response
from models import token as models
from util import tokens
from fastapi.responses import JSONResponse

from config.settings import settings

router = APIRouter()


@router.post("/tokens/", response_model=response.TokenCreated, tags=["tokens"])
@router.post("/tokens", response_model=response.TokenCreated, tags=["tokens"])
async def create_token_endpoint(token: models.Token, request: Request):
    """
    Create a token based on an existing set of clientId and secret.
    And this path operation will:

    * Create a token using existing credentials.
    * Returns the token to be used by the client.
    """
    created = tokens.create_token(identifier=token.client_id[0], secret=token.secret)
    resp = {"authorization": f"Bearer {created}"}
    if settings.ENV.lower() == "kubernetes":
        https_url = request.url.replace(scheme="https")
        headers = {"Location": str(https_url)}
        return JSONResponse(status_code=200, content=resp, headers=headers)

    else:
        return JSONResponse(status_code=200, content=resp)
