from fastapi import APIRouter
from schemas.notification import NotificationRequestSchema
from services import NotificationServiceDep

router = APIRouter()


@router.post('/send_notification', description='Send email notification')
async def send_notification(data: NotificationRequestSchema, service: NotificationServiceDep) -> dict:
    print('start')
    await service.handle(data)
    return {'status': 'Notification published'}

# todo отправить сообщение о регистрации
