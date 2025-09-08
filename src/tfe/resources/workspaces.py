from __future__ import annotations
from ._base import _Service
from ..types import Workspace, ExecutionMode


def _ws_from(d, org: str | None = None) -> Workspace:
    attr = d.get("attributes", {})
    return Workspace(
        id=d.get("id"),
        name=attr.get("name"),
        organization=org or attr.get("organization"),
        execution_mode=ExecutionMode(attr.get("execution-mode"))
        if attr.get("execution-mode")
        else None,
        project_id=attr.get("project", {}).get("id")
        if isinstance(attr.get("project"), dict)
        else None,
        tags=attr.get("tags", []) or [],
    )


class Workspaces(_Service):
    def list(self, organization: str, *, search: str | None = None):
        params = {}
        if search:
            params["search[name]"] = search
        path = f"/api/v2/organizations/{organization}/workspaces"
        for item in self._list(path, params=params):
            yield _ws_from(item, organization)

    def get(self, id_or_name: str, organization: str | None = None) -> Workspace:
        if organization:
            r = self.t.request(
                "GET", f"/api/v2/organizations/{organization}/workspaces/{id_or_name}"
            )
        else:
            r = self.t.request("GET", f"/api/v2/workspaces/{id_or_name}")
        return _ws_from(r.json()["data"], organization)

    def create(
        self,
        organization: str,
        name: str,
        *,
        execution_mode: str | None = "remote",
        project_id: str | None = None,
        tags: list[str] | None = None,
    ) -> Workspace:
        body = {"data": {"type": "workspaces", "attributes": {"name": name}}}
        if execution_mode:
            body["data"]["attributes"]["execution-mode"] = execution_mode
        if project_id:
            body["data"]["relationships"] = {
                "project": {"data": {"type": "projects", "id": project_id}}
            }
        if tags:
            body["data"]["attributes"]["tags"] = tags
        r = self.t.request(
            "POST", f"/api/v2/organizations/{organization}/workspaces", json_body=body
        )
        return _ws_from(r.json()["data"], organization)

    def update(self, id: str, **attrs) -> Workspace:
        body = {"data": {"type": "workspaces", "id": id, "attributes": {}}}
        for k, v in attrs.items():
            body["data"]["attributes"][k.replace("_", "-")] = v
        r = self.t.request("PATCH", f"/api/v2/workspaces/{id}", json_body=body)
        return _ws_from(r.json()["data"], None)

    def delete(self, id: str) -> None:
        self.t.request("DELETE", f"/api/v2/workspaces/{id}")
