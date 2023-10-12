import json
from typing import Annotated
from uuid import UUID

from fastapi import WebSocket, Depends

from core.logger import get_logger
from schemas.mailing import WebsocketMessageSchema

logger = get_logger()


class ConnectionManager:
    def __init__(self):
        self.connections: dict[UUID, WebSocket] = dict()

    def connect(self, websocket: WebSocket, user_id: UUID):
        logger.debug('Client connected: %s.', str(user_id))
        self.connections[user_id] = websocket

    def disconnect(self, user_id: UUID):
        logger.debug('Client disconnected: %s.', str(user_id))
        try:
            del self.connections[user_id]
        except KeyError:
            pass

    async def send_message(self, message: WebsocketMessageSchema, user_id: UUID):
        _logger = get_logger(message.request_id)
        try:
            websocket = self.connections[user_id]
            await websocket.send_text(json.dumps(message.model_dump(mode='json')))
            _logger.debug('Sent websocket message to user [%s]: %s - %s',
                          str(user_id), message.subject, message.body)
        except KeyError:
            _logger.debug('User [%s] is offline, can\'t send websocket message, skipping...',
                          str(user_id))


__ws_conn_mgr = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    return __ws_conn_mgr


ConnectionManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]

__all__ = ['ConnectionManagerDep',
           'ConnectionManager',
           'get_connection_manager']
