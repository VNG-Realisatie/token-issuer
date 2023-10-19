import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from config.settings import settings
from models import response

router = APIRouter()


@router.get(
    "/status/",
    response_model=response.Health,
    responses={400: {"model": response.Health}},
    tags=["status"],
)
@router.get(
    "/status",
    response_model=response.Health,
    responses={400: {"model": response.Health}},
    tags=["status"],
)
async def check_health(request: Request):
    """
    Check health before creating tokens:

    * Returns a boolean.
    """
    code = 400
    status = settings.ZGW_CLIENT.check_availability_of_apis()
    if status:
        code = 200

    if settings.ENV.lower() == "kubernetes":
        https_url = request.url.replace(scheme="https")
        headers = {"Location": str(https_url)}
        return JSONResponse(status_code=code, content={"health": status}, headers=headers)

    else:
        return JSONResponse(status_code=code, content={"health": status})
