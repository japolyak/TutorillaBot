import os
from dotenv import load_dotenv

load_dotenv()

# App
is_development = os.getenv("IS_DEVELOPMENT", "False") == "True"
app_port = int(os.getenv("APP_PORT") or 80)
api_link = os.getenv("API_LINK", "http://127.0.0.1:8000")

# Telegram
token = os.getenv("BOT_TOKEN", "")
webhook_enabled = os.getenv("USE_WEBHOOK", "True") == "True"
webhook_url = os.getenv("WEBHOOK_URL", "")
web_app_link = os.getenv("WEB_APP_LINK", "")

# REDIS
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_db = int(os.getenv("REDIS_DB", 0))
redis_password = os.getenv("REDIS_PASSWORD")
redis_username = os.getenv("REDIS_USERNAME")

