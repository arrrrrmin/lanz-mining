from pathlib import Path

import pytest


@pytest.fixture
def file() -> Path:
    return Path("tests/data/guests.csv")
