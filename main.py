from fastapi import FastAPI
from api.v1.api import api_router, tags_metadata
from config.settings import settings
from starlette.middleware.cors import CORSMiddleware
import logging


description = """
Token Issuer API helps you to create and propagate tokens to APIS. 🚀

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

app.include_router(api_router, prefix=settings.API_V1_STR)
