from uuid import UUID

from src.models import ViewsMessage


class ViewsMessageTransformer:
    @staticmethod
    def transform(message_key: bytes, message_body: bytes, message_timestamp: int) -> ViewsMessage:
        user_id, movie_id = (UUID(id_) for id_ in message_key.decode().split('+'))
        movie_timestamp = int(message_body.decode())
        return ViewsMessage(ts=movie_timestamp, user_id=user_id,
                            movie_id=movie_id, created=message_timestamp)
