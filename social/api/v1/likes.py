from fastapi import APIRouter

router = APIRouter()


@router.get('/ping')
def healthcheck():
    return 'pong!'
