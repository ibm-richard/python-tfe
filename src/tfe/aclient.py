"""
Async TFE Client: This client should not be used for now.
"""

from __future__ import annotations

from ._http import HTTPTransport
from .config import TFEConfig


class AsyncTFEClient:
    def __init__(self, config: TFEConfig | None = None):
        cfg = config or TFEConfig.from_env()
        self._transport = HTTPTransport(
            cfg.address,
            cfg.token,
            timeout=cfg.timeout,
            verify_tls=cfg.verify_tls,
            user_agent_suffix=cfg.user_agent_suffix,
            max_retries=cfg.max_retries,
            backoff_base=cfg.backoff_base,
            backoff_cap=cfg.backoff_cap,
            backoff_jitter=cfg.backoff_jitter,
            http2=cfg.http2,
            proxies=cfg.proxies,
            ca_bundle=cfg.ca_bundle,
        )
