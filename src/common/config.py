import os
from dotenv import load_dotenv


load_dotenv()


log_level = os.getenv("LOG_LEVEL", "DEBUG")
is_development = os.getenv("IS_DEVELOPMENT", "False") == "True"
api_link = os.getenv("API_LINK", "http://127.0.0.1:8000")

# App
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173&http://127.0.0.1:4040&http://127.0.0.1:5173&http://localhost:4040").split('&')

# Telegram
bot_token = os.getenv("BOT_TOKEN", "")
webhook_enabled = os.getenv("USE_WEBHOOK", "True") == "True"
webhook_url = os.getenv("WEBHOOK_URL", "")
web_app_link = os.getenv("WEB_APP_LINK")
dev_tg_id = int(os.getenv("DEV_TG_ID", 0))
admin_tg_id = int(os.getenv("ADMIN_TG_ID", 0))

# Database
_database_username = os.getenv(f"DB_USER")
_database_password = os.getenv(f"DB_PASSWORD")
database_host = os.getenv(f"DB_HOST")
database_port = int(os.getenv("DB_PORT") or 5432)
database_name = os.getenv(f"DB_NAME")
sqlalchemy_database_url = f"postgresql+psycopg2://{_database_username}:{_database_password}@{database_host}:{database_port}/{database_name}"

# REDIS
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_db = int(os.getenv("REDIS_DB", 0))
redis_password = os.getenv("REDIS_PASSWORD")
redis_username = os.getenv("REDIS_USERNAME")
