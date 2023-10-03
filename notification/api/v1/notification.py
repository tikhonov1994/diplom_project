from fastapi import APIRouter

router = APIRouter()


@router.post('/test', description='Test')
async def send_review() -> dict:
    return {'ok': True}
