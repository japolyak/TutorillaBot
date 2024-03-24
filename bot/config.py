import os

app_port = int(os.getenv("APP_PORT") or 80)
webhook_enabled = bool(os.getenv("USE_WEBHOOK") or False)
webhook_url = os.getenv("WEBHOOK_URL")
token = os.getenv("BOT_TOKEN")
api_link = os.getenv("API_LINK") or "http://127.0.0.1:8000"
web_app_link = os.getenv("WEB_APP_LINK")

# REDIS
redis_host = os.getenv("REDIS_HOST") or "localhost"
redis_db = int(os.getenv("REDIS_DB") or 0)
redis_password = os.getenv("REDIS_PASSWORD") or None
redis_username = os.getenv("REDIS_USERNAME") or None
