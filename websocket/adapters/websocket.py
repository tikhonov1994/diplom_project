from typing import Annotated
from uuid import UUID

from fastapi import WebSocket, Depends

from core.logger import get_logger

logger = get_logger()


class ConnectionManager:
    def __init__(self):
        self.connections: dict[UUID, WebSocket] = dict()

    def connect(self, websocket: WebSocket, user_id: UUID):
        logger.debug(f'Client connected: {str(user_id)}.')
        self.connections[user_id] = websocket

    def disconnect(self, user_id: UUID):
        logger.debug(f'Client disconnected: {str(user_id)}.')
        try:
            del self.connections[user_id]
        except KeyError:
            pass

    async def send_message(self, message: str, user_id: UUID):
        try:
            websocket = self.connections[user_id]
            await websocket.send_text(message)
        except KeyError:
            pass


__ws_conn_mgr = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    return __ws_conn_mgr


ConnectionManagerDep = Annotated[ConnectionManager, Depends(get_connection_manager)]

__all__ = ['ConnectionManagerDep',
           'ConnectionManager']
