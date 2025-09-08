from __future__ import annotations

from ..types import Project
from ._base import _Service


class Projects(_Service):
    def list(self, organization: str):
        path = f"/api/v2/organizations/{organization}/projects"
        for item in self._list(path):
            attr = item.get("attributes", {})
            yield Project(
                id=item.get("id"), name=attr.get("name"), organization=organization
            )
