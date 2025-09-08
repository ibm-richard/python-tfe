from typing import Optional, List, Dict

class TFEError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        errors: Optional[List[Dict]] = None,
    ):
        super().__init__(message)
        self.status = status
        self.errors = errors or []

class AuthError(TFEError): ...
class NotFound(TFEError): ...
class RateLimited(TFEError):
    def __init__(self, message: str, *, retry_after: Optional[float] = None, **kw):
        super().__init__(message, **kw)
        self.retry_after = retry_after
class ValidationError(TFEError): ...
class ServerError(TFEError): ...
class UnsupportedInCloud(TFEError): ...
class UnsupportedInEnterprise(TFEError): ...
