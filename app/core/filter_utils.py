from collections.abc import Callable

from sqlalchemy.orm import Query


def apply_filter(query: Query, filters: dict[str, Callable], args: dict) -> Query:
    for name, query_filter in filters.items():
        if name in args:
            try:
                query = query.filter(query_filter(args[name]))
            except Exception:
                raise ValueError(f"Ошибочный параметр {name}")

    return query
