from typing import Annotated

from fastapi import FastAPI, Request, Header
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from http import HTTPStatus

from core.config import app_config


def configure_tracer(app: FastAPI) -> None:
    if not app_config.enable_tracer:
        return

    @app.middleware('http')
    async def before_request(request: Request, call_next):
        response = await call_next(request)
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            return ORJSONResponse(status_code=HTTPStatus.BAD_REQUEST,
                                  content={'detail': 'X-Request-Id is required'})
        return response

    trace_resource = Resource(attributes={'service.name': 'auth_service'})
    trace.set_tracer_provider(TracerProvider(resource=trace_resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=app_config.jaeger_host,
                agent_port=app_config.jaeger_port
            )
        )
    )

    if app_config.debug:
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    FastAPIInstrumentor.instrument_app(app)


def inject_request_id(request_id: Annotated[str, Header(alias='X-Request-Id')]) -> None:
    if app_config.enable_tracer:
        current_span = trace.get_current_span()
        current_span.set_attribute('http.request_id', request_id)


def sub_span(func):
    if not app_config.enable_tracer:
        return func

    async def wrapped(*args, **kwargs):
        _tracer = trace.get_tracer(__name__)
        with _tracer.start_as_current_span(f'{func.__module__}.{func.__name__}'):
            return await func(*args, **kwargs)

    return wrapped
