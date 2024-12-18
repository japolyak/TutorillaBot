# from fastapi import FastAPI, HTTPException, Request
# from telebot.types import Update
#
# from core.bot.bot import bot
#
#
# app = FastAPI()
#
#
# @app.post("/bot_webhook")
# async def bot_webhook(request: Request):
#     if "content-type" not in request.headers or request.headers["content-type"] != "application/json":
#         raise HTTPException(status_code=400, detail="Bad request")
#
#     body_bytes = await request.body()
#
#     json_string = body_bytes.decode('utf-8')
#
#     update = Update.de_json(json_string)
#
#     bot.process_new_updates([update])
