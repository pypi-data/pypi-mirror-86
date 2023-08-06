import json
import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from web_error.error import HttpException


logger = logging.getLogger(__name__)


def exception_handler(request: Request, exc: Exception):
    status = 500
    message = "Unhandled exception occured."
    response = {
        "message": message,
        "debug_message": str(exc),
        "code": None,
    }

    if isinstance(exc, RequestValidationError):
        response["message"] = "Request validation error."
        response["debug_message"] = json.loads(exc.json())
        status = 422

    if isinstance(exc, HttpException):
        response = exc.marshal()
        status = exc.status

    if status >= 500:
        logger.exception(message, exc_info=(type(exc), exc, exc.__traceback__))

    return JSONResponse(
        status_code=status,
        content=response,
    )
