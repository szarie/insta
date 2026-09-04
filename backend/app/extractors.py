from __future__ import annotations

from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class ExtractionError(Exception):
    """An expected failure while retrieving public platform metadata."""


def identify_platform(url: str) -> str:
    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    if host in {"youtube.com", "m.youtube.com", "youtu.be"}:
        return "youtube"
    if host in {"instagram.com"}:
        return "instagram"
    raise ExtractionError("Only Instagram and YouTube links are supported.")


def validate_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ExtractionError("Enter a complete http(s) URL.")
    identify_platform(url)
    return url.strip()


class _MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        attributes = dict(attrs)
        key = attributes.get("property") or attributes.get("name")
        content = attributes.get("content")
        if key and content and key in {"og:description", "description", "twitter:description"}:
            self.values.setdefault(key, content)


def _fetch(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; DescriptionExtractor/1.0)",
            "Accept": "text/html,application/json",
        },
    )
    try:
        with urlopen(request, timeout=10) as response:
            return response.read(2_000_000).decode("utf-8", errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise ExtractionError("The public page could not be reached right now.") from exc


def _metadata_description(document: str) -> str:
    parser = _MetadataParser()
    parser.feed(document)
    description = (
        parser.values.get("og:description")
        or parser.values.get("description")
        or parser.values.get("twitter:description")
        or ""
    )
    # Keep paragraph breaks and intentional spacing from the original caption.
    return description.replace("\r\n", "\n").replace("\r", "\n").strip()


def extract_youtube(url: str) -> str:
    description = _metadata_description(_fetch(url))
    if not description:
        raise ExtractionError(
            "No public description was found. The YouTube video may be unavailable."
        )
    return description


def extract_instagram(url: str) -> str:
    description = _metadata_description(_fetch(url))
    if not description:
        raise ExtractionError(
            "No public description was found. The Instagram post may be private or unavailable."
        )
    return description


def extract_description(url: str) -> tuple[str, str]:
    normalized_url = validate_url(url)
    platform = identify_platform(normalized_url)
    extractor = extract_youtube if platform == "youtube" else extract_instagram
    return platform, extractor(normalized_url)
