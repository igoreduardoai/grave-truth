"""Local URL allowlist. Public hosts are rejected unless the code is changed."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost"})


def is_local_prefix(prefix: str) -> bool:
    parsed = urlparse(prefix)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.hostname in LOCAL_HOSTS
        and not parsed.username
        and not parsed.password
    )


def navigation_allowed(url: str, page_url: str = "http://127.0.0.1/") -> bool:
    """True for same-page hashes and http(s) URLs on localhost or 127.0.0.1."""
    if not url or url.startswith("#"):
        return True
    absolute = urljoin(page_url, url)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return False
    if parsed.username or parsed.password:
        return False
    return parsed.hostname in LOCAL_HOSTS
