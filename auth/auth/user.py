from fastapi import APIRouter, HTTPException, Query
from starlette import status

from services.user import UserServiceDep


router = APIRouter()


@router.post('/register', description='Регистрация пользователя')
async def user_registration(service: UserServiceDep, email: str, password: str) -> None:
    pass
