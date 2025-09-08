from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ..types import Organization
from ._base import _Service


def _safe_str(v: Any, default: str = "") -> str:
    return v if isinstance(v, str) else (str(v) if v is not None else default)


class Organizations(_Service):
    def list(self) -> Iterator[Organization]:
        for item in self._list("/api/v2/organizations"):
            attr = item.get("attributes", {}) or {}
            org_id = _safe_str(item.get("id"))
            name = _safe_str(attr.get("name") or item.get("id"))
            email = attr.get("email") if isinstance(attr.get("email"), str) else None
            yield Organization(id=org_id, name=name, email=email)

    def get(self, name: str) -> Organization:
        r = self.t.request("GET", f"/api/v2/organizations/{name}")
        d = r.json()["data"]
        attr = d.get("attributes", {}) or {}
        org_id = _safe_str(d.get("id"))
        org_name = _safe_str(attr.get("name") or d.get("id"))
        email = attr.get("email") if isinstance(attr.get("email"), str) else None
        return Organization(id=org_id, name=org_name, email=email)
