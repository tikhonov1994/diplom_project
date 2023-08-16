from pydantic import BaseModel


class IndexItemList(BaseModel):
    count: int
    total_pages: int
    prev: int | None
    next: int | None
    results: list
