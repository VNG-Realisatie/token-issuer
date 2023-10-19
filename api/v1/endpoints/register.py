import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from config.settings import settings
from models import response
from models import user as models
from util import randomizer, tokens

router = APIRouter()


@router.post(
    "/register/",
    response_model=response.TokenPropagated,
    responses={400: {"model": response.BadRequest}},
    tags=["register"],
)
@router.post(
    "/register",
    response_model=response.TokenPropagated,
    responses={400: {"model": response.BadRequest}},
    tags=["register"],
)
async def create_propagated_user(user: models.User, request: Request):
    """
    Create the requested client_ids with different APIs.

    This will register the client_id with the authorization api and then propagate the secret and id
    to the different APIs.

    And this path operation will:

    * Create a token to be able to register with the different APIs.
    * Register with the authorization API.
    * Register the client_ids with the available APIs if it has the `heeftAlleAutorisaties` bool:
        - BRC
        - NRC
        - ZTC
        - AC
        - ZRC
        - DRC
    * Else it will register with those apis that are part of the `autorisaties` dict in the request.
    * Create a token with the client_ids and secret
    * Returns the token to be used by the client.
    """

    user_ids = []
    for client_id in user.clientIds:
        user_ids.append(randomizer.create_random_id(client_id))

    user.clientIds = user_ids

    ac_token = tokens.create_token(
        identifier=settings.TOKEN_ISSUER_IDENTIFIER,
        secret=settings.TOKEN_ISSUER_SECRET,
    )

    body = user.to_dict()

    settings.ZGW_CLIENT.autorisatie.set_token(token=ac_token)
    created = settings.ZGW_CLIENT.autorisatie.create_user(body=body)

    if created.status_code != 201:
        if settings.ENV.lower() == "kubernetes":
            https_url = request.url.replace(scheme="https")
            headers = {"Location": str(https_url)}
            return JSONResponse(status_code=400, content={"message": created.json()}, headers=headers)

        else:
            return JSONResponse(status_code=400, content={"message": created.json()})


    logging.debug(f"got a response {str(created.status_code)} when creating new user")
    logging.info(
        f"created client_id {created.json()['clientIds']} in the autorisatieapi"
    )

    secret = randomizer.create_random_string(size=32)
    settings.ZGW_CLIENT.set_token(token=ac_token)

    if not user.heeftAlleAutorisaties:
        propagated = settings.ZGW_CLIENT.propagate_to_authorized_apis(
            client_ids=user_ids, secret=secret, authorization=user.autorisaties
        )
    else:
        propagated = settings.ZGW_CLIENT.propagate_to_all_apis(user_ids, secret)

    logging.info(f"propagated to all apis result: {str(propagated)}")

    token = tokens.create_token(user_ids[0], secret)
    propagated_list = [
        {
            "endpoint": propagation.endpoint,
            "success": propagation.success,
            "client_id": propagation.client_id,
        }
        for propagation in propagated
    ]

    if settings.ENV.lower() == "kubernetes":
        https_url = request.url.replace(scheme="https")
        headers = {"Location": str(https_url)}
        logging.info(https_url)
        logging.info(headers)
        return JSONResponse(status_code=200, content={"authorization": f"Bearer {token}", "propagated": propagated_list}, headers=headers)

    else:
        return JSONResponse(status_code=200, content={"authorization": f"Bearer {token}", "propagated": propagated_list})
