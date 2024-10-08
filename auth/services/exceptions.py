from uuid import UUID


class ServiceExceptionBase(Exception):
    pass


class ServiceSingleElementException(ServiceExceptionBase):
    def __init__(self, item_name: str, item_id: UUID) -> None:
        super().__init__()
        self._item_name = item_name
        self._item_id = item_id


class ServiceItemNotFound(ServiceSingleElementException):
    def __str__(self) -> str:
        return f'Can\'t find {self._item_name} with id: \'{self._item_id}\''


class ServiceItemSearchException(ServiceExceptionBase):
    def __init__(self, item_name: str, search_field: str, search_val: any) -> None:
        self._item_name = item_name
        self._s_field = search_field
        self._s_val = search_val

    def __str__(self) -> str:
        return f'Can\'t find {self._item_name} with \'{self._s_field}\' == \'{self._s_val}\''


class ServiceUniqueFieldViolation(ServiceItemSearchException):
    def __str__(self) -> str:
        return f'{self._item_name} with \'{self._s_field}\' = \'{self._s_val}\' already exists'


class ServiceConflictOnAddError(ServiceExceptionBase):
    def __init__(self, item_dict: dict[str, any]) -> None:
        self._schema_json = item_dict

    def __str__(self) -> str:
        return f'Failed to add object: \'{self._schema_json}\''


class ServiceConflictOnDeleteError(ServiceSingleElementException):
    def __str__(self) -> str:
        return f'Can\'t delete {self._item_name} with id: ' \
               f'\'{self._item_id}\': db conflict'
