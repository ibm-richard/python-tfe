from __future__ import annotations

from .._base import _AService, _Service


class AdminSettings(_Service):
    def terraform_versions(self):
        r = self.t.request("GET", "/api/v2/admin/terraform-versions")
        return r.json()


class AdminSettingsAsync(_AService):
    async def terraform_versions(self):
        r = await self.t.arequest("GET", "/api/v2/admin/terraform-versions")
        return r.json()
