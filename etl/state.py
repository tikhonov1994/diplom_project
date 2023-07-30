import abc
from typing import Any, Dict
import json
import os


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

        with open(self.file_path, 'w+') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""

        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, 'r') as file:
                data = file.read()
                data = json.loads(data)
                return data
        except json.JSONDecodeError:
            return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = storage.retrieve_state()

    def set_state(self, key: str, value: any) -> None:
        self.state[key] = value
        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        current_state = self.state
        if len(current_state) == 0 or key not in current_state:
            return None

        return current_state[key]
