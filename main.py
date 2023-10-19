import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from api.v1.api import api_router, tags_metadata
from api.base.api import redirect_router
from config.settings import settings

description = """
Token Issuer API helps you to create and propagate tokens to APIS. 🚀

This API no longer has a GUI so it must be approached as a RESTful api.

For more information see:

https://github.com/VNG-Realisatie/token-issuer

## Token

You will be able to:

* **Create tokens**.

## Register

You will be able to:

* **Propagate users to apis**.
"""

app = FastAPI(
    title="zgw-token-issuer",
    description=description,
    version=settings.VERSION,
    terms_of_service="https://vng-realisatie.github.io/gemma-zaken/beheer/gebruiksvoorwaarden",
    contact={
        "name": "VNG Realisatie",
        "url": "https://vng-realisatie.github.io/gemma-zaken",
        "e-mail": "standaarden.ondersteuning@vng.nl",
    },
    license_info={
        "name": "EUPL 1.2",
        "url": "https://opensource.org/licenses/EUPL-1.2",
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    trusting_proxy=True,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.HOSTS
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(redirect_router)


if __name__ == "__main__":
    reload = False
    port = int(settings.PORT)
    log_level = logging.WARNING
    if settings.ENV.lower() == "local":
        reload = True

    if settings.ENV.lower() == "local" or settings.ENV.lower() == "kubernetes":
        log_level = logging.DEBUG

    uvicorn.run(
        "main:app", port=port, reload=reload, log_level=log_level, use_colors=True, host="0.0.0.0"
    )
