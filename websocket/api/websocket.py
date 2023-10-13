from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from adapters.websocket import ConnectionManagerDep
from core.auth import UserIdDep

router = APIRouter(prefix='/websocket', tags=['websocket'])


@router.websocket("/notify")
async def websocket_endpoint(websocket: WebSocket,
                             conn_manager: ConnectionManagerDep,
                             user_id: UserIdDep) -> None:
    conn_manager.connect(websocket, user_id)
    try:
        await websocket.accept()
        while True:
            _ = await websocket.receive()
    except (WebSocketDisconnect, RuntimeError):
        conn_manager.disconnect(user_id)
