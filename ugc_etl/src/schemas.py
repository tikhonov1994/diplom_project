from typing import Union, List
from pydantic import BaseModel, Field


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
    exceptions: Union[List[str], str] = None
    trace_id: str = None
    span_id: str = None
    parent_id: str = None

    class Config:
        allow_population_by_field_name = True
