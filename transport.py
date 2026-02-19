import os
import json
import logging
from typing import Any, Optional
import requests
from requests import Response, Session

LOG = logging.getLogger("oc_skill.transport")

_ENV_BASE: dict[str, str] = {
    "ENV_PROD":    "https://my.opalstack.com/api/v1",
    "ENV_STAGING": "https://my.opalstack.live/api/v1",
    "ENV_DEV":     "https://my.opalstack.me/api/v1",
}

def resolve_base_url() -> str:
    for flag, url in _ENV_BASE.items():
        if os.getenv(flag):
            return url
    return "https://my.opalstack.com/api/v1"

BASE_URL: str = resolve_base_url()


class Transport:
    """Connection-reusing JSON client. Non-2xx raises RuntimeError."""

    def __init__(self, token: str, timeout: float = 10.0) -> None:
        self.session: Session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Content-Type":  "application/json",
            "Accept":        "application/json",
            "User-Agent":    "oc-skill/0.1",
        })
        self.timeout = timeout

    def _handle(self, resp: Response) -> Any:
        if not 200 <= resp.status_code < 300:
            try:
                payload = resp.json()
            except ValueError:
                payload = resp.text
            LOG.error("HTTP %s → %s", resp.status_code, payload)
            raise RuntimeError(payload)
        try:
            return resp.json()
        except ValueError as exc:
            raise RuntimeError("non-JSON response") from exc

    def get(self, path: str, params: Optional[dict] = None) -> Any:
        r = self.session.get(BASE_URL + path, params=params, timeout=self.timeout)
        return self._handle(r)

    def post(self, path: str, body: Any = None) -> Any:
        r = self.session.post(BASE_URL + path,
                              data=json.dumps(body or {}),
                              timeout=self.timeout)
        return self._handle(r)
