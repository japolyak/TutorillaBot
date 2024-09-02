import os
from dotenv import load_dotenv


load_dotenv()


log_level = os.getenv("LOG_LEVEL", "DEBUG")
is_development = os.getenv("IS_DEVELOPMENT", "False") == "True"
api_link = os.getenv("API_LINK", "http://127.0.0.1:8000")
_timeout = os.getenv("TIMEOUT")
api_timeout = int(_timeout) if _timeout is not None else None

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split('&')

# Telegram
bot_token = os.getenv("BOT_TOKEN", "")
use_webhook = os.getenv("USE_WEBHOOK", "True") == "True"
webhook_url = os.getenv("WEBHOOK_URL", "")
web_app_link = os.getenv("WEB_APP_LINK")
admin_tg_id = int(os.getenv("ADMIN_TG_ID"))

# Database
_database_username = os.getenv(f"DB_USER", "postgres")
_database_password = os.getenv(f"DB_PASSWORD", "postgres")
_database_host = os.getenv(f"DB_HOST", "127.0.0.1")
_database_port = int(os.getenv("DB_PORT") or 5432)
_database_name = os.getenv(f"DB_NAME", "postgres")
sqlalchemy_database_url = f"postgresql+psycopg2://{_database_username}:{_database_password}@{_database_host}:{_database_port}/{_database_name}"

# REDIS
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_db = int(os.getenv("REDIS_DB", 0))
redis_password = os.getenv("REDIS_PASSWORD")
redis_username = os.getenv("REDIS_USERNAME")
