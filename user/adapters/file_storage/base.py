from abc import ABC, abstractmethod


class BaseFileStorage(ABC):
    @abstractmethod
    async def save(self, origin_file_name: str, image_bytes: bytes, content_type: str) -> str:
        raise NotImplemented

    @abstractmethod
    async def load(self, image_url: str) -> bytes:
        raise NotImplemented
