import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.common.config import allowed_origins
from src.common.logger import configure_logger

from src.api.src.database.db_setup import initialize_database
from src.api.src.router import api_router


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
