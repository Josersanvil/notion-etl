import pytest

from notion_etl.loader import NotionDataLoader


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            ("authorization", "Bearer secret_..."),
            ("user-agent", None),
            ("cookie", None),
        ],
    }


@pytest.fixture
def database_ids() -> dict[str, str]:
    """Fixture to provide a dictionary of database IDs."""
    return {
        "blog_post_2_page": "1eaff0a4-106e-8024-a1b0-eac74b216928",
        "simple_database": "1eaff0a4106e800f808dfe8b13ae6b9e",
        "database_with_relations": "1eaff0a4106e8089a040d23b1fab810b",
    }


@pytest.fixture
def notion_loader():
    """Fixture to initialize the NotionDataLoader."""
    return NotionDataLoader()
