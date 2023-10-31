from abc import ABC, abstractmethod


class BaseSyncFileStorage(ABC):
    @abstractmethod
    def save(self, origin_file_name: str, image_bytes: bytes, content_type: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def load(self, image_url: str) -> bytes:
        raise NotImplementedError
