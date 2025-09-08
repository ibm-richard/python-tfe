from __future__ import annotations

from ..types import Organization
from ._base import _Service


class Organizations(_Service):
    def list(self):
        for item in self._list("/api/v2/organizations"):
            attr = item.get("attributes", {})
            yield Organization(
                id=item.get("id"),
                name=attr.get("name") or item.get("id"),
                email=attr.get("email"),
            )

    def get(self, name: str) -> Organization:
        r = self.t.request("GET", f"/api/v2/organizations/{name}")
        d = r.json()["data"]
        attr = d.get("attributes", {})
        return Organization(
            id=d.get("id"),
            name=attr.get("name") or d.get("id"),
            email=attr.get("email"),
        )
