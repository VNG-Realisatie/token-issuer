from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url="redoc")
    return response
