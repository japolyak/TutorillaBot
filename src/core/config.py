import os
from dotenv import load_dotenv
from pathlib import Path

dot_env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dot_env_path)

log_level = os.getenv("LOG_LEVEL", "DEBUG")
is_development = os.getenv("IS_DEVELOPMENT", "0") == "1"
api_link = os.getenv("API_LINK", "http://127.0.0.1:8000")
access_token_ttl_in_minutes = 15
refresh_token_ttl_in_days = 7

# API
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173&http://127.0.0.1:5173").split('&')
algorithm = os.getenv("ALGORITHM", "HS256")

# Telegram
bot_token = os.getenv("BOT_TOKEN", "")
web_app_link = os.getenv("WEB_APP_LINK")
admin_tg_id = int(os.getenv("ADMIN_TG_ID"))
support_nick = os.getenv("SUPPORT_NICK")

# Database
_database_username = os.getenv(f"DB_USER", "postgres")
_database_password = os.getenv(f"DB_PASSWORD", "postgres")
_database_name = os.getenv(f"DB_NAME", "postgres")
_database_host = os.getenv(f"DB_HOST", "localhost")
_database_port = int(os.getenv(f"DB_PORT", 5432))
schema_name = "core"
connection_string = f"postgresql+psycopg2://{_database_username}:{_database_password}@{_database_host}:{_database_port}/{_database_name}"

# REDIS
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_db = 0
redis_username = "default"
