from abc import ABC, abstractmethod
from enum import Enum

from schemas.image import UserImageSchema


class NsfwCheckResult(str, Enum):
    accepted = 'ACCEPTED'
    non_accepted = 'NON_ACCEPTED'


class BaseNsfwChecker(ABC):
    @abstractmethod
    async def check(self, image: UserImageSchema) -> NsfwCheckResult:
        raise NotImplementedError
