import os
import statistics_bot.main as main

from fastapi import APIRouter, Request, responses
from telebot import types

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

router = APIRouter()

@router.post('/' + main.TOKEN)
async def get_message(request: Request):
    json_string = await request.json()
    update = types.Update.de_json(json_string)
    main.bot.process_new_updates([update])
    return 200
    

@router.get('/setwebhook')
async def webhook():
    main.bot.remove_webhook()
    await main.bot.set_webhook(url=WEBHOOK_URL + main.TOKEN)
    return "!", 200
    


@router.get('/ping')
def ping_server():
    return 200
