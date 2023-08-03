from typing import Annotated

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta

from starlette.responses import JSONResponse

# from jose import JWTError, jwt


router = APIRouter()

# todo сгенерить и положить в енв и конфиг
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

class User(BaseModel):
    id
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# хеширование и соление пароля
# def get_password_hash(password):
#     return pwd_context.hash(password)


def find_user_by_username(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(fake_db, username: str, password: str):
    user = find_user_by_username(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def fake_hash_password(password: str):
    return "fakehashed" + password

@router.post(
    path='/login',
    response_model=Token,
    description='Аутентификация юзера',
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    # todo проверить что креды валидные
    user_dict = fake_users_db.get(form_data.username)
    # if check_user_credentials():
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


    # переводим в модельку
    user = User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


    # todo сгенерить JWT

@router.post(
    path='/login',
    response_model=Token,
    description='Аутентификация юзера',
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    Authorize: AuthJWT = Depends()
) -> JSONResponse:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # создаем access token и refresh token
    # todo как генерить refresh-token?
    # todo записать в базу их?
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # )

    access_token = Authorize.create_access_token(subject=user.username, expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # todo Store refresh and access tokens in DB
    # todo set cookie

    # todo сохранить в историю входов в аккаунт

    # todo что писать в payload access tokena? - по идее надо роли записать, майл, user-agent,
    # return {"access_token": access_token, "token_type": "bearer"}
    return {'status': 'success', 'access_token': access_token}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

    # todo достать данные для новых токенов из БД через GenericStorage!
    # todo текущий рефреш токен удалить/отключить
    current_user = Authorize.get_jwt_subject()

    new_access_token = Authorize.create_access_token(subject=current_user)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user)

    # todo save to redis
    # todo что делать с рефреш токеном? - удалить, либо поле is_active
    return {"new_access_token": new_access_token}

