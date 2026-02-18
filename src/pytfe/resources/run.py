from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ..errors import (
    InvalidOrgError,
    InvalidRunIDError,
    InvalidWorkspaceIDError,
    RequiredWorkspaceError,
    TerraformVersionValidForPlanOnlyError,
)
from ..models.run import (
    Run,
    RunApplyOptions,
    RunCancelOptions,
    RunCreateOptions,
    RunDiscardOptions,
    RunForceCancelOptions,
    RunListForOrganizationOptions,
    RunListOptions,
    RunReadOptions,
)
from ..utils import _safe_str, valid_string, valid_string_id
from ._base import _Service


class Runs(_Service):
    def list(
        self, workspace_id: str, options: RunListOptions | None = None
    ) -> Iterator[Run]:
        """List all the runs of the given workspace."""
        if not valid_string_id(workspace_id):
            raise InvalidWorkspaceIDError()
        params = options.model_dump(by_alias=True) if options else {}
        path = f"/api/v2/workspaces/{workspace_id}/runs"
        for item in self._list(path, params=params):
            attrs = item.get("attributes", {})
            attrs["id"] = item.get("id")
            yield Run.model_validate(attrs)

    def list_for_organization(
        self, organization: str, options: RunListForOrganizationOptions | None = None
    ) -> Iterator[Run]:
        """List all the runs of the given organization."""
        if not valid_string_id(organization):
            raise InvalidOrgError()
        path = f"/api/v2/organizations/{organization}/runs"
        params = options.model_dump(by_alias=True, exclude_none=True) if options else {}
        # meta = jd.get("meta", {})
        # pagination = meta.get("pagination", {})
        for item in self._list(path, params=params):
            attrs = item.get("attributes", {})
            attrs["id"] = item.get("id")
            yield Run.model_validate(attrs)

    def create(self, options: RunCreateOptions) -> Run:
        """Create a new run for the given workspace."""
        if options.workspace is None:
            raise RequiredWorkspaceError()
        if valid_string(options.terraform_version) and (
            options.plan_only is None or not options.plan_only
        ):
            raise TerraformVersionValidForPlanOnlyError()
        attrs = options.model_dump(by_alias=True, exclude_none=True)
        body: dict[str, Any] = {
            "data": {
                "attributes": attrs,
                "type": "runs",
            }
        }
        if options.workspace:
            body["data"]["relationships"] = {
                "workspace": {
                    "data": {
                        "type": "workspaces",
                        "id": options.workspace.id,
                    }
                }
            }
        if options.configuration_version:
            if "relationships" not in body["data"]:
                body["data"]["relationships"] = {}
            body["data"]["relationships"]["configuration-version"] = {
                "data": {
                    "type": "configuration-versions",
                    "id": options.configuration_version.id,
                }
            }
        r = self.t.request(
            "POST",
            "/api/v2/runs",
            json_body=body,
        )
        d = r.json().get("data", {})
        attrs = d.get("attributes", {})
        return Run(
            id=_safe_str(d.get("id")),
            **{k.replace("-", "_"): v for k, v in attrs.items()},
        )

    def read(self, run_id: str) -> Run:
        """Read a run by its ID."""
        return self.read_with_options(run_id)

    def read_with_options(
        self, run_id: str, options: RunReadOptions | None = None
    ) -> Run:
        """Read a run by its ID with the given options."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        params: dict[str, Any] = {}
        if options and options.include:
            params["include"] = ",".join(options.include)
        r = self.t.request(
            "GET",
            f"/api/v2/runs/{run_id}",
            params=params,
        )
        d = r.json().get("data", {})
        attrs = d.get("attributes", {})
        return Run(
            id=_safe_str(d.get("id")),
            **{k.replace("-", "_"): v for k, v in attrs.items()},
        )

    def apply(self, run_id: str, options: RunApplyOptions | None = None) -> None:
        """Apply a run by its ID."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        body = {"comment": options.comment} if options and options.comment else None
        self.t.request("POST", f"/api/v2/runs/{run_id}/actions/apply", json_body=body)

        return None

    def cancel(self, run_id: str, options: RunCancelOptions | None = None) -> None:
        """Cancel a run by its ID."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        body = {"comment": options.comment} if options and options.comment else None
        self.t.request("POST", f"/api/v2/runs/{run_id}/actions/cancel", json_body=body)
        return None

    def force_cancel(
        self, run_id: str, options: RunForceCancelOptions | None = None
    ) -> None:
        """ForceCancel is used to forcefully cancel a run by its ID."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        body = {"comment": options.comment} if options and options.comment else None
        self.t.request(
            "POST", f"/api/v2/runs/{run_id}/actions/force-cancel", json_body=body
        )
        return None

    def force_execute(self, run_id: str) -> None:
        """ForceExecute is used to forcefully execute a run by its ID."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        self.t.request("POST", f"/api/v2/runs/{run_id}/actions/force-execute")
        return None

    def discard(self, run_id: str, options: RunDiscardOptions | None = None) -> None:
        """Discard a run by its ID."""
        if not valid_string_id(run_id):
            raise InvalidRunIDError()
        body = {"comment": options.comment} if options and options.comment else None
        self.t.request("POST", f"/api/v2/runs/{run_id}/actions/discard", json_body=body)
        return None
