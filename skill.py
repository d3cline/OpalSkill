import os
from .transport import Transport


class SkillBase:
    """Base for all Opalstack skill tools.

    Reads OPALSTACK_API_TOKEN from the environment once per tool call.
    Subclasses call self._transport() to get an authenticated Transport.
    """

    def _token(self) -> str:
        token = os.getenv("OPALSTACK_API_TOKEN", "")
        if not token:
            raise RuntimeError("OPALSTACK_API_TOKEN env var not set")
        return token

    def _transport(self) -> Transport:
        return Transport(token=self._token())
