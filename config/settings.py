import configparser
import logging
import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from client import zgw
from models import endpoints


class Settings(BaseSettings):
    PORT = os.environ.get("PORT", "8000")
    logging.info(f"port set to {PORT}")
    ENV = os.environ.get("ENV", "test")
    logging.info(f"env set to {ENV}")
    config = configparser.ConfigParser()
    config.read("config.ini")
    logging.info(f"config set to {config[ENV]}")
    zgw_endpoints = endpoints.end_points_from_dict(config[ENV])
    logging.info(f"endpoints set to {zgw_endpoints}")

    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    TOKEN_ISSUER_SECRET: str = os.environ.get("TOKEN_ISSUER_SECRET")
    TOKEN_ISSUER_IDENTIFIER: str = os.environ.get("TOKEN_ISSUER_IDENTIFIER")
    ZGW_CLIENT = zgw.Client(endpoints=zgw_endpoints)

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("TOKEN_ISSUER_SECRET", allow_reuse=True)
    def secret_check(cls, v: str):
        if v is None:
            raise ValueError(v)
        return v

    @validator("TOKEN_ISSUER_IDENTIFIER", allow_reuse=True)
    def identity_check(cls, v: str):
        if v is None:
            raise ValueError(v)
        return v


settings = Settings()
logging.info(settings)
