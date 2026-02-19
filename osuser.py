from typing import Literal, Any, Dict
import logging

from .transport import Transport
from .skill import SkillBase

logger = logging.getLogger("oc_skill.osuser")


class OSUserAPI:
    def __init__(self, token: str) -> None:
        self.http = Transport(token=token)

    def list(self) -> list:
        return self.http.get("/osuser/list/")

    def read(self, data: Dict[str, Any]) -> dict:
        return self.http.get(f"/osuser/read/{data['id']}")

    def create(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/osuser/create/", [data])

    def update(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/osuser/update/", [data])

    def delete(self, data: Dict[str, Any]) -> Any:
        return self.http.post("/osuser/delete/", [data])


class OSUserTools(SkillBase):
    def osuser(
        self,
        action: Literal["list", "read", "create", "update", "delete"],
        payload: Any | None = None,
    ):
        """---
        name: osusers
        description: |
            Manages OS shell users on an Opalstack web server.
            Applications depend on an OSUser to run.
            Parent: Server (WEB).  All mutating calls auto-wrap payload in a list.

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
                summary: Return all OS users visible to the token.
                payload: null
            read:
                summary: Fetch an OS user by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            create:
                summary: Create a new OS user on a server.
                payload:
                    required: [name, server]
                    properties:
                        name:   { type: string }
                        server: { type: string, format: uuid }
            update:
                summary: Update OS user attributes.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            delete:
                summary: Remove an OS user by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
        ...
        """
        api = OSUserAPI(token=self._token())
        return {
            "list":   lambda _: api.list(),
            "read":   api.read,
            "create": api.create,
            "update": api.update,
            "delete": api.delete,
        }[action](payload or {})
