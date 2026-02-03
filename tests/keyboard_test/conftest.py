import pytest


@pytest.fixture
def year_and_month() -> tuple[int, int]:
    return (2026, 1)
