from fastapi import APIRouter
from schemas.mailing import CreateMailingRequestSchema, UserRegisterMailingSchema, \
    UpdateMailingStatusRequestSchema
from services import MailingServiceDep

router = APIRouter()


@router.post('/send', description='Create mailing')
async def send(data: CreateMailingRequestSchema, service: MailingServiceDep) -> dict:
    await service.handle(data)
    return {'status': 'Mailing created'}


@router.post('/welcome_user', description='Send welcome email to registered user')
async def send_registration(data: UserRegisterMailingSchema, service: MailingServiceDep) -> dict:
    mailing_data = await service.get_registration_mailing_data(data.user_id, data.email)

    await service.handle(mailing_data)

    return {'status': 'Notification published'}


@router.post('/update_status', description='Update mailing status')
async def update_status(data: UpdateMailingStatusRequestSchema, service: MailingServiceDep) -> dict:

    await service.update_status(data.mailing_id, data.status)

    return {'status': 'Status updated'}
