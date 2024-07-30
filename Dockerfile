FROM python:3.12

ENV PYTHONUNBUFFERED True

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn src.bot.main:app --host 0.0.0.0 --port $PORT
