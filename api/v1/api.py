from fastapi import APIRouter
from api.v1.endpoints import tokens, register

# this is used to create tags in the swagger and openapi docs
tags_metadata = [
    {
        "name": "register",
        "description": "Propagate a clientIds and secret over multiple APIs",
    },
    {
        "name": "tokens",
        "description": "Create tokens based on **existing** secrets.",
        "externalDocs": {
            "description": "More information about JWT",
            "url": "https://jwt.io/",
        },
    },
]

api_router = APIRouter()
api_router.include_router(tokens.router)
api_router.include_router(register.router)
