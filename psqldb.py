from typing import Literal, Any, Dict
import logging

from .transport import Transport
from .skill import SkillBase

logger = logging.getLogger("oc_skill.psqldb")


class PSQLDBAPI:
    def __init__(self, token: str) -> None:
        self.http = Transport(token=token)

    def list(self) -> list:
        return self.http.get("/psqldb/list/")

    def read(self, data: Dict[str, Any]) -> dict:
        return self.http.get(f"/psqldb/read/{data['id']}")

    def create(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/psqldb/create/", [data])

    def update(self, data: Dict[str, Any]) -> dict:
        return self.http.post("/psqldb/update/", [data])

    def delete(self, data: Dict[str, Any]) -> Any:
        return self.http.post("/psqldb/delete/", [data])


class PSQLDBTools(SkillBase):
    def psqldb(
        self,
        action: Literal["list", "read", "create", "update", "delete"],
        payload: Any | None = None,
    ):
        """---
        name: psqldbs
        description: |
            Manages PostgreSQL databases on Opalstack.
            To use a database, create a PSQLUser then grant permissions via update.
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
                summary: Return all PostgreSQL databases visible to the token.
                payload: null
            read:
                summary: Fetch a database by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
            create:
                summary: Create a new PostgreSQL database on a server.
                payload:
                    required: [name, server]
                    properties:
                        name:   { type: string }
                        server: { type: string, format: uuid }
            update:
                summary: Update user permissions on the database.
                payload:
                    required: [id]
                    properties:
                        id:                  { type: string, format: uuid }
                        dbusers_readwrite:   { type: array, items: { type: string, format: uuid } }
                        dbusers_readonly:    { type: array, items: { type: string, format: uuid } }
            delete:
                summary: Remove a database by UUID.
                payload:
                    required: [id]
                    properties:
                        id: { type: string, format: uuid }
        ...
        """
        api = PSQLDBAPI(token=self._token())
        return {
            "list":   lambda _: api.list(),
            "read":   api.read,
            "create": api.create,
            "update": api.update,
            "delete": api.delete,
        }[action](payload or {})
