import polars as pl
import pytest

from notion_etl.database import NotionDataset


@pytest.mark.vcr()
def test_get_database_as_dataset(notion_loader, database_ids: dict[str, str]):
    """Test get_database method returning a NotionDataset."""
    database_id = database_ids["simple_database"]
    result = notion_loader.get_database(database_id=database_id)
    assert isinstance(result, NotionDataset)
    assert result.size == 4


@pytest.mark.vcr()
def test_get_simple_database_as_df(notion_loader, database_ids: dict[str, str]):
    """Test get_database method with a Polars DataFrame."""
    database_id = database_ids["simple_database"]
    result = notion_loader.get_database(database_id=database_id)
    df = result.to_dataframe(clean=True)
    assert isinstance(df, pl.DataFrame)
    expected_schema = {
        "Description": pl.Utf8,
        "Tags": pl.List(pl.Utf8),
        "Name": pl.Utf8,
        "_page_id": pl.Utf8,
        "_page_url": pl.Utf8,
        "_page_public_url": pl.Utf8,
        "_created_at": pl.Datetime(),
        "_last_edited_at": pl.Datetime(),
    }
    assert df.shape == (4, 8)
    assert dict(df.schema) == expected_schema


@pytest.mark.vcr()
def test_get_database_with_relations_as_df(notion_loader, database_ids: dict[str, str]):
    """Test get_database method on a database with relations on a Polars DataFrame."""
    database_id = database_ids["database_with_relations"]
    result = notion_loader.get_database(database_id=database_id)
    df = result.to_dataframe(clean=True)
    assert isinstance(df, pl.DataFrame)
    expected_schema = {
        "Post tags": pl.Struct(
            [
                pl.Field("type", pl.Utf8),
                pl.Field(
                    "multi_select",
                    pl.List(
                        pl.Struct(
                            [
                                pl.Field("id", pl.Utf8),
                                pl.Field("name", pl.Utf8),
                                pl.Field("color", pl.Utf8),
                            ]
                        )
                    ),
                ),
            ]
        ),
        "Post description": pl.Struct(
            [
                pl.Field("type", pl.Utf8),
                pl.Field(
                    "rich_text",
                    pl.List(
                        pl.Struct(
                            [
                                pl.Field("type", pl.Utf8),
                                pl.Field(
                                    "text",
                                    pl.Struct(
                                        [
                                            pl.Field("content", pl.Utf8),
                                            pl.Field("link", pl.Null),
                                        ]
                                    ),
                                ),
                                pl.Field(
                                    "annotations",
                                    pl.Struct(
                                        [
                                            pl.Field("bold", pl.Boolean),
                                            pl.Field("italic", pl.Boolean),
                                            pl.Field("strikethrough", pl.Boolean),
                                            pl.Field("underline", pl.Boolean),
                                            pl.Field("code", pl.Boolean),
                                            pl.Field("color", pl.Utf8),
                                        ]
                                    ),
                                ),
                                pl.Field("plain_text", pl.Utf8),
                                pl.Field("href", pl.Null),
                            ]
                        )
                    ),
                ),
            ]
        ),
        "Rating": pl.Utf8,
        "Post": pl.Utf8,
        "Name": pl.Utf8,
        "_page_id": pl.Utf8,
        "_page_url": pl.Utf8,
        "_page_public_url": pl.Utf8,
        "_created_at": pl.Datetime(time_unit="us", time_zone=None),
        "_last_edited_at": pl.Datetime(time_unit="us", time_zone=None),
    }
    assert df.shape == (5, 10)
    assert dict(df.schema) == expected_schema
    records = df.select("Post").to_dicts()
    records[0]["Post"] == "1eaff0a4-106e-80ad-8f7a-f4fb5d0e3a20"
