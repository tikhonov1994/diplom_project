from uuid import UUID
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import json

from core.auth import UserIdDep


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.connections: dict[UUID, WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: UUID):
        self.connections[user_id] = websocket

    async def disconnect(self, user_id: UUID):
        try:
            del self.connections[user_id]
        except KeyError:
            pass

    async def broadcast(self, data: str):
        # broadcasting data to all connected clients
        for connection in self.connections.values():
            await connection.send_json(data)
    
    async def send_personal_message(self, message: str, user_id: UUID):
        try:
            websocket = self.connections[user_id]
        except KeyError:
            pass
        await websocket.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: UserIdDep):
    print('sdsdf')
    await manager.connect(websocket, user_id)
    try:
        while True:
            # here we are waiting for an oncomming message from clients
            
            await websocket.send('PING')
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except:
        pass