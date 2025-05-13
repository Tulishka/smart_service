from collections.abc import Callable

from sqlalchemy.orm import Query


def apply_filter(query: Query, filters: dict[str, Callable], args: dict) -> Query:
    """Добавляет набор фильтров к запросу

    :param query: запрос которому необходимо добавить фильтры
    :param filters: словарь с описанием возможных фильтров. Значение в словаре это функция f(val),
                    которая возвращает выражение для подстановки в метод: Query.filter(f(val))
    :param args: словарь, содержащий значения для подстановки в фильтр
    :return: возвращает новый Query
    """
    for name, query_filter in filters.items():
        if name in args:
            try:
                query = query.filter(query_filter(args[name]))
            except Exception:
                raise ValueError(f"Ошибочный параметр {name}")

    return query
