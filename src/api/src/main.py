import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.common.logger import log
from src.common.config import allowed_origins

from src.api.src.router import api_router
from src.api.src.exception_handlers import apply_exception_handlers


log.info(msg="Starting app...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

apply_exception_handlers(app)
