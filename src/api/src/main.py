import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.config import allowed_origins
from .database.db_setup import initialize_database

from router import api_router
from src.common.logger import configure_logger


log = logging.getLogger(__name__)

configure_logger()

log.info(msg="Starting app...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()
app.include_router(api_router)
