import logging

from fastapi import APIRouter
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
async def check_health():
    """
    Check health before creating tokens:

    * Returns a boolean.
    """
    code = 400
    status = settings.ZGW_CLIENT.check_availability_of_apis()
    if status:
        code = 200
    return JSONResponse(status_code=code, content={"health": status})
