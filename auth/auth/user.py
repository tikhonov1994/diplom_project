from fastapi import APIRouter, HTTPException, Query
from starlette import status

from db.model import UserInfo
from services.user import UserServiceDep


router = APIRouter()


@router.post('/register', response_model=UserInfo, description='Регистрация пользователя')
async def user_registration(service: UserServiceDep, email: str, password: str):
    pass
