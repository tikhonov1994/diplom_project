from pydantic import BaseModel, Field, ConfigDict


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

    model_config = ConfigDict(populate_by_name=True)
