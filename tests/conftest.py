import pytest
from spoons_api.repositories.venues import all as get_all_venues


@pytest.fixture(scope="session")
def venue_summaries():
    return get_all_venues()
