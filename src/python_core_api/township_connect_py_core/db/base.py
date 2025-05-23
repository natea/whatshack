from sqlalchemy.orm import DeclarativeBase

from township_connect_py_core.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
