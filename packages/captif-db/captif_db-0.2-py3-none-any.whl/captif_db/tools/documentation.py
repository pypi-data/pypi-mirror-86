"""
Documentation helpers.
"""

from typing import Union
from eralchemy import render_er
from itertools import chain
from pathlib import Path

from captif_db import Base


def table_tags() -> dict:
    """
    List tags by table name. Used to generate the database ER diagrams.

    """
    return {tt: mm.info.get("er_tags", []) for tt, mm in Base.metadata.tables.items()}


def unique_tags() -> set:
    """
    Generate a list of unique table tags. Used to generate the database ER diagrams.

    """
    return set(chain(*[tt for tt in table_tags().values()]))


def tag_tables() -> dict:
    """
    List tables by tag. Used to generate the database ER diagrams.

    """
    return {
        tag: [table for table, tags in table_tags().items() if tag in tags]
        for tag in unique_tags()
    }


def save_graphs(path: Union[str, Path]):
    """
    Generate database ER diagrams. Creates one diagram with all tables and separate
    diagrams for each table tag.

    :param path: Base file for storing diagrams. The tag is appended to the base
        filename when saving the tag-specific diagrams.

    """
    if ~isinstance(path, Path):
        path = Path(path)

    render_er(Base, path.as_posix())
    for tag, tables in tag_tables().items():
        path_ = path.with_name(f"{path.stem}_{tag}{path.suffix}")
        render_er(Base, path_.as_posix(), include_tables=tables)
