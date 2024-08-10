FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

WORKDIR /src

COPY src/bot /src/bot
COPY src/common /src/common

WORKDIR /src/bot

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn src.main:app --host 0.0.0.0 --port $PORT
