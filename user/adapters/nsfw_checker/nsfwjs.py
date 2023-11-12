from io import BytesIO
from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient

from adapters.nsfw_checker.base import BaseNsfwChecker, NsfwCheckResult
from core.config import app_config
from core.logger import logger
from schemas.image import UserImageSchema, NsfwPredictionList
from schemas.image import NsfwPredictionClass as PredClass

_PERMISSION_WEIGHTS = {
    PredClass.sexy: 0.9,
    PredClass.porn: 0.5,
    PredClass.drawing: 0.5,
    PredClass.hentai: 0.3,
    PredClass.neutral: 1.0
}


class NsfwJSChecker(BaseNsfwChecker):
    async def check(self, image: UserImageSchema) -> NsfwCheckResult:
        files = {'content': (image.name, BytesIO(image.data), image.mime)}
        async with AsyncClient(verify=False) as client:
            response = await client.post(url=app_config.nsfw.url, files=files)
            response.raise_for_status()
        return self.__grant_permission(NsfwPredictionList.model_validate(response.json()))

    @staticmethod
    def __grant_permission(predictions: NsfwPredictionList) -> NsfwCheckResult:
        if app_config.debug:
            logger.debug(predictions.model_dump_json())

        if any(pred.probability > _PERMISSION_WEIGHTS[pred.class_name] for pred in predictions.predictions):
            return NsfwCheckResult.non_accepted
        return NsfwCheckResult.accepted


NsfwJSCheckerDep = Annotated[NsfwJSChecker, Depends()]
