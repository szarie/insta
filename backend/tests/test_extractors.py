import pytest

from backend.app.extractors import (
    ExtractionError,
    _metadata_description,
    identify_platform,
    validate_url,
)


def test_identifies_supported_platforms() -> None:
    assert identify_platform("https://www.youtube.com/watch?v=abc") == "youtube"
    assert identify_platform("https://instagram.com/p/abc/") == "instagram"


def test_rejects_unsupported_hosts() -> None:
    with pytest.raises(ExtractionError):
        validate_url("https://example.com/post")


def test_preserves_metadata_line_breaks() -> None:
    html = '<meta property="og:description" content="First line&#10;&#10;Second line">'
    assert _metadata_description(html) == "First line\n\nSecond line"
