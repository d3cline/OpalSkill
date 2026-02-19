from typing import Literal, Any, Dict
import logging

from .transport import Transport
from .skill import SkillBase

logger = logging.getLogger("oc_skill.domain")


class DomainAPI:
    def __init__(self, token: str) -> None:
        self.http = Transport(token=token)

    def list(self) -> list:
        return self.http.get("/domain/list/")

    def read(self, data: Dict[str, Any]) -> dict:
        return self.http.get(f"/domain/read/{data['id']}")

    def create(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/domain/create/", [data])

    def update(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/domain/update/", [data])

    def delete(self, data: Dict[str, Any]) -> Any:
        return self.http.post("/domain/delete/", [data])


class DomainTools(SkillBase):
    def domain(
        self,
        action: Literal["list", "read", "create", "update", "delete"],
        payload: Any | None = None,
    ):
        """---
        name: domains
        description: |
            Manages domain and subdomain names on Opalstack.
            A Domain object must exist before creating a Site that uses it.
            All mutating calls auto-wrap payload in a list.

        parameters:
            type: object
            properties:
                action:
                    type: string
                    enum: [list, read, create, update, delete]
                payload:
                    type: [object, "null"]
            required: [action]

        actions:
            list:
                summary: Return all domains visible to the token.
                payload: null
            read:
                summary: Fetch a domain by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            create:
                summary: Add a new domain or subdomain.
                payload:
                    required: [name]
                    properties:
                        name: { type: string, description: "Fully qualified domain name." }
            update:
                summary: Update domain name by UUID.
                payload:
                    required: [id]
                    properties:
                        id:   { type: string, format: uuid }
                        name: { type: string }
            delete:
                summary: Remove a domain by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
        ...
        """
        api = DomainAPI(token=self._token())
        return {
            "list":   lambda _: api.list(),
            "read":   api.read,
            "create": api.create,
            "update": api.update,
            "delete": api.delete,
        }[action](payload or {})
