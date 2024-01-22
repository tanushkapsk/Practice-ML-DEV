from typing import Any

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    id = mapped_column(Integer, primary_key=True)

    # Generate DB table name automatically
    @declared_attr
    def __tablename__(cls) -> str:
        module_name = '_'.join(filter(lambda x: x not in ['app', 'models'], cls.__module__.split('.')))
        return f'{module_name}_{cls.__name__.lower()}'

    @declared_attr
    def __fk_column__(cls) -> str:
        return f"{cls.__tablename__}.id"

    type_annotation_map = {
        dict[str, Any]: JSON,
        list[dict[str, Any]]: JSON
    }
