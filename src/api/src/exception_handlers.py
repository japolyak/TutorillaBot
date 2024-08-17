from fastapi import FastAPI, Request

from src.api.src.bot_client.message_sender import send_error_message
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.utils.string_utils import StringUtils
from src.common.config import admin_tg_id


def apply_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception):
        message = StringUtils.create_error_message(exc)

        send_error_message(admin_tg_id, message)

        return ResponseBuilder.error_response(500, message='An unexpected error occurred.')
