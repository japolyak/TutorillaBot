import os

app_port = int(os.getenv("APP_PORT") or 1234)
webhook_enabled = bool(os.getenv("USE_WEBHOOK"))
webhook_url = os.getenv("WEBHOOK_URL")
token = os.getenv("BOT_TOKEN" or "empty")
api_link = os.getenv("FASTAPI_API" or "empty")
web_app_link = os.getenv("WEB_APP_LINK" or "empty")
redis_host = os.getenv("REDIS_HOST" or "empty")
redis_port = os.getenv("REDIS_PORT" or 1235)
