
import pytest
from pydantic import ValidationError

from app.schemas import PostingRequest


def test_valid_message():
    request = PostingRequest(
        message="Check this out https://example.com"
    )
    assert request.cta_url == "https://example.com"


def test_message_without_url():
    with pytest.raises(ValidationError):
        PostingRequest(message="Hello everyone")


def test_message_with_multiple_urls():
    with pytest.raises(ValidationError):
        PostingRequest(
            message="Visit https://example.com and https://google.com"
        )


def test_message_over_200_characters():
    with pytest.raises(ValidationError):
        PostingRequest(
            message="A" * 201 + " https://example.com"
        )


def test_invalid_url():
    with pytest.raises(ValidationError):
        PostingRequest(message="Visit https://invalid")
