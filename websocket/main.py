from fastapi import FastAPI
import uvicorn
import sentry_sdk

from api.websocket import router as ws_router
from core.config import app_config as cfg
from core.middleware import LoggingMiddleware
from core.logger import get_logger

logger = get_logger()

if cfg.export_logs:
    sentry_sdk.init(
        dsn=cfg.sentry_dsn,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1
    )


app = FastAPI()
app.middleware('http')(LoggingMiddleware())
app.include_router(ws_router)


######################################
from fastapi.responses import HTMLResponse

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8011/websocket/notify?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMmJiODg5Yy00MzkzLTQyMGMtOGE0Yy1hMTczMTVhMzE4MTQiLCJpYXQiOjE2OTcwMzM3NTQsIm5iZiI6MTY5NzAzMzc1NCwianRpIjoiZjAyZjEyYzYtNWNkNC00YzgwLTg1YzAtMzVjNzM5MWVjZjlkIiwiZXhwIjoxNjk3MDM0OTU0LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJyb2xlIjoidXNlciIsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE3LjAuMC4wIFNhZmFyaS81MzcuMzYiLCJyZWZyZXNoX2p0aSI6ImY2ODczMWM4LWE5M2EtNDAwZi1hYzA2LWIxZTkwNTRhN2U5NCJ9.saXTqdXrB2sYFsyM9pzcwrtudk7luCVxZ3ugFO8ju08");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)
######################################


if __name__ == '__main__':
    logger.info(f'%s is up and running at %s:%d.',
                cfg.ws.project_name,
                cfg.ws.host,
                cfg.ws.port)
    uvicorn.run(
        'main:app',
        host=cfg.ws.host,
        port=cfg.ws.port,
    )
