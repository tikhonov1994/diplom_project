from enum import Enum
from datetime import date


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
                 filter_value: date | int | None = None) -> None:
        self.order = order
        self.filter_field = filter_field
        self.filter_argument = filter_argument
        self.filter_value = filter_value
    