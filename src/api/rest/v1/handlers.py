import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

from application.exception import (
    ApplicationError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    ServiceUnavailableError,
    UnprocessableEntityError,
)

logger = logging.getLogger(__name__)

_APPLICATION_ERROR_STATUSES: dict[type[ApplicationError], HTTPStatus] = {
    NotFoundError: HTTPStatus.NOT_FOUND,
    ConflictError: HTTPStatus.CONFLICT,
    UnprocessableEntityError: HTTPStatus.UNPROCESSABLE_ENTITY,
    InternalServerError: HTTPStatus.INTERNAL_SERVER_ERROR,
    ServiceUnavailableError: HTTPStatus.SERVICE_UNAVAILABLE,
}


def _server_error_response(
    request: Request,
    exc: Exception,
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
) -> JSONResponse:
    logger.error(
        "Request failed: %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status_code,
        content={"detail": status_code.phrase},
    )


async def application_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Map application errors and their subclasses to HTTP responses."""
    status_code = next(
        (
            code
            for error_type, code in _APPLICATION_ERROR_STATUSES.items()
            if isinstance(exc, error_type)
        ),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    if status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        return _server_error_response(request, exc, status_code)

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc) or status_code.phrase},
    )


async def custom_http_exception_handler(
    request: Request,
    exc: Exception,
) -> Response:
    """Preserve HTTP status, detail, headers and responses without a body."""
    assert isinstance(exc, HTTPException)
    return await http_exception_handler(request, exc)


async def custom_request_validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Return FastAPI's standard 422 response for invalid request data."""
    assert isinstance(exc, RequestValidationError)
    return await request_validation_exception_handler(request, exc)


async def internal_server_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Log unexpected failures and keep their details out of the response."""
    return _server_error_response(request, exc)


def initialize_exception_handlers(app: FastAPI) -> None:
    """Register HTTP exception handlers before the application starts."""
    app.add_exception_handler(ApplicationError, application_exception_handler)
    # FastAPI's HTTPException inherits from Starlette's HTTPException.
    app.add_exception_handler(HTTPException, custom_http_exception_handler)
    app.add_exception_handler(
        RequestValidationError,
        custom_request_validation_exception_handler,
    )
    app.add_exception_handler(
        ResponseValidationError,
        internal_server_exception_handler,
    )
    app.add_exception_handler(Exception, internal_server_exception_handler)
