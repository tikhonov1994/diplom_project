from typing import Union, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseJsonLogSchema(BaseModel):
    """
    Main log in JSON format
    """
    thread: Union[int, str]
    level_name: str
    message: str
    source_log: str
    timestamp: str = Field(..., alias='@timestamp')
    app_name: str
    app_version: str
    duration: int
    exceptions: Optional[Union[List[str], str]] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    parent_id: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class RequestJsonLogSchema(BaseModel):
    """
    Schema for request/response answer
    """
    request_uri: str
    request_referer: str
    request_method: str
    request_path: str
    request_host: str
    request_size: int
    request_content_type: str
    request_headers: dict
    request_direction: str
    response_status_code: int
    response_size: int
    response_headers: dict
    duration: int
