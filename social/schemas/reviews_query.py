from datetime import datetime
from enum import Enum


class Order(str, Enum):
    added_asc = 'added_asc'
    added_desc = 'added_desc'
    author_rating_asc = 'author_rating_asc'
    author_rating_desc = 'author_rating_desc'


class FilterField(str, Enum):
    added = 'added'
    author_rating = 'author_rating'


class FilterArgument(str, Enum):
    gt = 'gt'
    gte = 'gte'
    lt = 'lt'
    lte = 'lte'


class QueryParams:
    def __init__(self, order: Order = Order.added_asc,
                 filter_field: FilterField | None = None,
                 filter_argument: FilterArgument | None = None,
                 date_value: datetime | None = None,
                 rating_value: int | None = None) -> None:
        self.order = order
        self.filter_field = filter_field
        self.filter_argument = filter_argument
        self.date_value = date_value
        self.rating_value = rating_value
    