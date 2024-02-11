import os

app_port = int(os.getenv("APP_PORT"))
webhook_enabled = bool(os.getenv("USE_WEBHOOK"))
webhook_url = os.getenv("WEBHOOK_URL")
token = os.getenv("BOT_TOKEN")
api_link = os.getenv("FASTAPI_API")
web_app_link = os.getenv("WEB_APP_LINK")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
