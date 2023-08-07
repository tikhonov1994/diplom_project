from core.config import app_config as config


# async def create_tokens(self) -> tuple[str, str]:
#     access_token = Authorize.create_access_token(
#         subject=user.username,
#         expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     refresh_token = Authorize.create_refresh_token(
#         subject=str(user.id),
#         expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
#         user_claims={
#             'role': user_role,
#             'login': us er.login,
#         }
#     )

    # return 'wqe'


    # def decode_token(self, token):
    #     try:
    #         payload = jwt.decode(token, self.secret, algorithms=['HS256'])
    #         if (payload['scope'] == 'access_token'):
    #             return payload['sub']
    #         raise HTTPException(status_code=401, detail='Scope for the token is invalid')
    #     except jwt.ExpiredSignatureError:
    #         raise HTTPException(status_code=401, detail='Token expired')
    #     except jwt.InvalidTokenError:
    #         raise HTTPException(status_code=401, detail='Invalid token')