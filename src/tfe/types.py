from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ExecutionMode(str, Enum):
    REMOTE = "remote"
    AGENT = "agent"
    LOCAL = "local"


class RunStatus(str, Enum):
    PLANNING = "planning"
    PLANNED = "planned"
    APPLIED = "applied"
    CANCELED = "canceled"
    ERRORED = "errored"


class Organization(BaseModel):
    id: str
    name: str
    email: str | None = None


class Project(BaseModel):
    id: str
    name: str
    organization: str


class Workspace(BaseModel):
    id: str
    name: str
    organization: str
    execution_mode: ExecutionMode | None = None
    project_id: str | None = None
    tags: list[str] = []
