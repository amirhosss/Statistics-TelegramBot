import os

import config
import statistics_bot.main as main

from fastapi import APIRouter, Request
from telebot import types


router = APIRouter()


@router.post('/' + main.TOKEN)
async def get_message(request: Request):
    json_string = await request.json()
    update = types.Update.de_json(json_string)
    main.bot.process_new_updates([update])
    return 200
    

@router.get('/setwebhook')
def webhook():
    main.bot.remove_webhook()
    main.bot.set_webhook(url=config.WEBHOOK_URL + main.TOKEN)
    return '!', 200
    

@router.get('/ping')
def ping_server():
    return 200
