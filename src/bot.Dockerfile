FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

WORKDIR /src

COPY bot /src/bot
COPY common /src/common

WORKDIR /src/bot

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src/bot/src

CMD ["python", "main.py"]
