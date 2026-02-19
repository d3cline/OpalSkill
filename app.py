from typing import Literal, Any, Dict
import logging

from .transport import Transport
from .skill import SkillBase

logger = logging.getLogger("oc_skill.app")

# ── installer catalogue (static, mirrors opalstack/installers on GitHub) ──────
INSTALLERS = [
    {"selected_type": "wordpress",  "name": "WordPress",         "app_type": "NPF",
     "url": {"el7": "https://raw.githubusercontent.com/opalstack/installers/master/core/wordpress/install.sh",
             "el9": "https://raw.githubusercontent.com/opalstack/installers/refs/heads/master/el9/wordpress/install.sh"},
     "json": {"auto_site_url": True, "fpm_max_requests": 250, "fpm_max_children": 25, "php_version": 83, "gzip": True, "expires": "off"}},
    {"selected_type": "laravel",    "name": "Laravel",           "app_type": "NPF",
     "url": {"el7": "https://raw.githubusercontent.com/opalstack/installers/master/core/laravel/install.py",
             "el9": "https://raw.githubusercontent.com/opalstack/installers/master/el9/laravel/install.py"},
     "json": {"fpm_max_requests": 250, "fpm_max_children": 25, "gzip": True, "php_version": 83, "subroot": "project/public", "expires": "off"}},
    {"selected_type": "nextjs",     "name": "Next.js",           "app_type": "CUS",
     "url": {"el7": "https://raw.githubusercontent.com/opalstack/installers/master/core/nextjs/install.py",
             "el9": "https://raw.githubusercontent.com/opalstack/installers/master/el9/nextjs/install.py"},
     "json": {"gzip": True, "expires": "off"}},
    {"selected_type": "ghost",      "name": "Ghost",             "app_type": "CUS",
     "url": {"el7": "https://raw.githubusercontent.com/opalstack/installers/master/core/ghost/install.py",
             "el9": "https://raw.githubusercontent.com/opalstack/installers/refs/heads/master/el9/ghost/install.py"},
     "json": {"gzip": True, "expires": "off"}},
    {"selected_type": "django",     "name": "Django",            "app_type": "CUS",
     "url": {"el9": "https://raw.githubusercontent.com/opalstack/installers/master/el9/django/install.py"},
     "json": {"gzip": True, "expires": "off"}},
    {"selected_type": "static_only","name": "Nginx Static Only", "app_type": "STA",
     "url": {},
     "json": {"gzip": True, "expires": "off"}},
]


class ApplicationAPI:
    def __init__(self, token: str) -> None:
        self.http = Transport(token=token)

    def list(self) -> list:
        return self.http.get("/app/list/")

    def read(self, data: Dict[str, Any]) -> dict:
        return self.http.get(f"/app/read/{data['id']}")

    def create(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/app/create/", [data])

    def update(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/app/update/", [data])

    def delete(self, data: Dict[str, Any]) -> Any:
        return self.http.post("/app/delete/", [data])


class ApplicationTools(SkillBase):
    def application(
        self,
        action: Literal["list", "read", "create", "update", "delete", "installer_urls"],
        payload: Any | None = None,
    ):
        """---
        name: applications
        description: |
            Manages web applications on the Opalstack platform.

            ⚠️  INSTALLER WORKFLOW — for any installer-based app:
              1. Call action "installer_urls" to get correct app_type and url.
              2. Create with those exact values.

            Parent: OSUser.  All mutating calls auto-wrap payload in a list.

        parameters:
            type: object
            properties:
                action:
                    type: string
                    enum: [list, read, create, update, delete, installer_urls]
                payload:
                    type: [object, "null"]
            required: [action]

        actions:
            list:
                summary: Return all applications visible to the token.
                payload: null
            read:
                summary: Fetch a single application by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            create:
                summary: Create a new application.
                payload:
                    required: [name, osuser, type]
                    properties:
                        name:          { type: string }
                        osuser:        { type: string, format: uuid }
                        type:          { type: string, description: "Base stack: NPF, CUS, APA, STA, etc." }
                        installer_url: { type: string, format: uri }
                        json:          { type: object }
            update:
                summary: Update an existing application by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            delete:
                summary: Remove an application by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            installer_urls:
                summary: Return the catalogue of available one-click installers.
                payload: null
        ...
        """
        api = ApplicationAPI(token=self._token())
        return {
            "list":           lambda _: api.list(),
            "read":           api.read,
            "create":         api.create,
            "update":         api.update,
            "delete":         api.delete,
            "installer_urls": lambda _: INSTALLERS,
        }[action](payload or {})
