from urllib.parse import urlparse


def validate_cta_url(url: str) -> bool:
    parsed = urlparse(url)

    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and "." in parsed.hostname if parsed.hostname else False
    )