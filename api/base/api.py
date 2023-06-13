from fastapi import APIRouter

from api.base.endpoints import redirect

redirect_router = APIRouter()
redirect_router.include_router(redirect.router)
