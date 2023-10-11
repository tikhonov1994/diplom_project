from uuid import UUID


class BaseStorageException(Exception):
    pass


class ItemNotFoundException(BaseStorageException):
    def __init__(self, item_id: UUID, table: str) -> None:
        super().__init__()
        self.item_id = item_id
        self.table = table

    def __str__(self) -> str:
        return f'Item with id: \'{self.item_id}\' not found in table \'{self.table}\''


class TemplateNotFoundException(BaseStorageException):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        return f'Template with name \'{self.name}\' not found'
