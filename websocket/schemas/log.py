from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator


class BaseJsonLogSchema(BaseModel):
    thread: int | str
    level_name: str
    message: str
    source_log: str
    timestamp: str = Field(..., alias='@timestamp')
    app_name: str
    app_version: str
    duration: int
    exceptions: list[str] | str = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None
    request_id: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class RequestJsonLogSchema(BaseModel):
    request_uri: str
    request_referer: str
    request_method: str
    request_path: str
    request_host: str
    request_size: int
    request_content_type: str
    request_headers: dict
    request_body: str | None
    request_direction: str
    response_status_code: int
    response_size: int
    response_headers: dict
    response_body: str | None
    duration: int
    request_id: UUID | None = None

    # noinspection PyMethodParameters
    @field_validator(
        'request_body',
        'response_body',
        mode='before',
    )
    def valid_body(cls, field):
        if isinstance(field, bytes):
            try:
                field = field.decode()
            except UnicodeDecodeError:
                field = b'file_bytes'
            return field

        if isinstance(field, str):
            return field
