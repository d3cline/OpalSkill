"""oc_skill — Opalstack API skill plugin for OpenClaw."""

from .app import ApplicationTools
from .domain import DomainTools
from .mariadb import MariaDBTools
from .psqldb import PSQLDBTools
from .osuser import OSUserTools

__all__ = [
    "ApplicationTools",
    "DomainTools",
    "MariaDBTools",
    "PSQLDBTools",
    "OSUserTools",
]

# Convenience: list of all tool classes for registration
TOOLS = [
    ApplicationTools,
    DomainTools,
    MariaDBTools,
    PSQLDBTools,
    OSUserTools,
]
