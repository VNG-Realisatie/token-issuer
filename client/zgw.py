import requests
from util.logger import logger

import models.user
from models.response import Propagation
from models.endpoints import EndPoints
from urllib.parse import urlparse, urljoin


class BaseClient:
    def __init__(self):
        self.application = "application/json"
        self.jwt_endpoint = "jwtsecret/"
        self.token = ""

    @staticmethod
    def create_url(base_url: str, path: str):
        if not base_url.endswith("/"):
            base_url = base_url + "/"
        return urljoin(base_url, path)

    def _get_header(self):
        return {
            "Accept": self.application,
            "Content-Type": self.application,
            "Authorization": f"Bearer {self.token}",
        }

    def set_token(self, token: str):
        self.token = token


class Client(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, endpoints: EndPoints):
        super().__init__()
        self.endpoints = endpoints
        self.autorisatie = AutorisatieApi(base_url=endpoints.ac)

    def propagate_to_all_apis(self, client_ids: list[str], secret: str):
        endpoints = self.endpoints.to_dict()
        success = []
        for key in endpoints:
            for client_id in client_ids:
                success.append(
                    self.register_with_api(endpoints[key], client_id, secret)
                )

        return success

    def propagate_to_authorized_apis(
        self,
        client_ids: list[str],
        secret: str,
        authorization: list[models.user.Authorization],
    ):
        endpoints = self.endpoints.to_dict()
        success = []
        for auth in authorization:
            for client_id in client_ids:
                success.append(
                    self.register_with_api(endpoints[auth.component.upper()], client_id, secret)
                        )
        return success

    def register_with_api(self, endpoint: str, client_id: str, secret: str):
        body = {"identifier": client_id, "secret": secret}
        method = "POST"
        url = self.create_url(base_url=endpoint, path=self.jwt_endpoint)
        print(url)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)

        logger.debug(f"response code {response.status_code} received from {url}")
        return Propagation(client_id=client_id, endpoint=endpoint, success=response.status_code == 201)


class AutorisatieApi(BaseClient):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, base_url: str):
        super().__init__()
        self.applicatie_endpoint = "applicaties"
        self.base_url = base_url

    def create_user(self, body: dict):
        method = "POST"
        url = self.create_url(base_url=self.base_url, path=self.applicatie_endpoint)
        header = self._get_header()
        response = requests.request(method, url, headers=header, json=body)
        return response
