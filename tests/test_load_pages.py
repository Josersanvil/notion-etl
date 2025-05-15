from pathlib import Path

import polars as pl
import pytest

from notion_etl.page import NotionPageContents

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.vcr()
def test_get_page_contents(notion_loader, database_ids: dict[str, str]):
    """Test get_page_contents method."""
    page_id = database_ids["blog_post_2_page"]
    page = notion_loader.get_page_contents(page_id=page_id)
    assert isinstance(page, NotionPageContents)
    assert len(page.contents) == 28


@pytest.mark.vcr()
def test_get_page_contents_as_df(notion_loader, database_ids: dict[str, str]):
    """Test get_page_contents method as a Polars DataFrame."""
    page_id = database_ids["blog_post_2_page"]
    page = notion_loader.get_page_contents(page_id=page_id)
    page_df = page.as_dataframe()
    expected_schema = {
        "block_number": pl.Int64,
        "id": pl.Utf8,
        "type": pl.Utf8,
        "plain_text": pl.Utf8,
        "created_time": pl.Datetime(time_unit="us", time_zone="UTC"),
        "last_edited_time": pl.Datetime(time_unit="us", time_zone="UTC"),
        "created_by": pl.Utf8,
        "last_edited_by": pl.Utf8,
        "color": pl.Utf8,
        "parent": pl.Utf8,
        "has_children": pl.Boolean,
        "archived": pl.Boolean,
        "in_trash": pl.Boolean,
        "compiled_md": pl.Utf8,
    }
    page_schema = dict(page_df.schema)
    page_schema.pop("rich_text")
    assert isinstance(page_df, pl.DataFrame)
    assert page_schema == expected_schema
    assert page_df.shape == (28, 15)


@pytest.mark.vcr()
def test_page_contents_as_plain_text(notion_loader, database_ids: dict[str, str]):
    """Test get_page_contents method as plain text."""
    page_id = database_ids["blog_post_2_page"]
    page = notion_loader.get_page_contents(page_id=page_id)
    page_text = page.as_plain_text()
    assert isinstance(page_text, str)
    with open(FIXTURES_DIR / "blog_post_2.txt") as f:
        expected_text = f.read()
    assert page_text == expected_text


@pytest.mark.vcr()
def test_page_contents_as_markdown(notion_loader, database_ids: dict[str, str]):
    """Test get_page_contents method as markdown."""
    page_id = database_ids["blog_post_2_page"]
    page = notion_loader.get_page_contents(page_id=page_id)
    page_md = page.as_markdown()
    assert isinstance(page_md, str)
    with open(FIXTURES_DIR / "blog_post_2.md") as f:
        expected_md = f.read()
    assert page_md == expected_md
