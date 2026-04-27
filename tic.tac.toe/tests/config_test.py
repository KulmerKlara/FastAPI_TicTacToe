import pytest

from app.core.config import Settings

# Testet, ob api key mapp richtig
def test_api_key_map_parsing():
    settings = Settings(
        DATABASE_URL="sqlite://",
        API_KEYS="alice:key1, bob:key2 , invalid_entry"
    )

    result = settings.api_key_map

    assert result == {
        "alice": "key1",
        "bob": "key2",
    }

# testet, ob richtiger key bei user in db gespeichert ist. 
def test_key_to_user_mapping():
    settings = Settings(
        DATABASE_URL="sqlite://",
        API_KEYS="alice:key1,bob:key2"
    )

    result = settings.key_to_user

    assert result == {
        "key1": "alice",
        "key2": "bob",
    }