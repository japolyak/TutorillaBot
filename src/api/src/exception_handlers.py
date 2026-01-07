from fastapi import FastAPI, Request
from telebot.apihelper import ApiTelegramException

from src.api.src.bot_client.message_sender import MessageSender
from src.api.src.builders.response_builder import ResponseBuilder

from src.core.string_utils import StringUtils
from src.core.config import admin_tg_id


def apply_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception):
        message = StringUtils.create_error_message(exc)

        disable_notification = isinstance(exc, ApiTelegramException)
        MessageSender.send_error_message(admin_tg_id, message, disable_notification)

        return ResponseBuilder.error_response(500, message='An unexpected error occurred.')
