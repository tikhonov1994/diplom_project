from typing import Annotated
from fastapi import Query

class PaginatedParams:
    def __init__(self, page_number: Annotated[int, Query(gt=0)] = 1,
                 page_size: Annotated[int, Query(gt=0, lt=10_000)] = 50) -> None:
        self.page_number = page_number
        self.page_size = page_size