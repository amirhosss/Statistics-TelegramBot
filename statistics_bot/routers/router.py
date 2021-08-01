import os
import statistics_bot.main as main

from pydantic import BaseModel
from fastapi import APIRouter, Request, responses
from telebot import types

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

router = APIRouter()

class Item(BaseModel):
    update_id: int
    message: types.Message

@router.post('/' + main.TOKEN)
def get_message(request: Item):
    print(request)
    update = types.Update.de_json(request)
    main.bot.process_new_updates([update])
    return 200
    

@router.get('/setwebhook')
def webhook():
    main.bot.remove_webhook()
    main.bot.set_webhook(url=WEBHOOK_URL + main.TOKEN)
    return '!', 200
    


@router.get('/ping')
def ping_server():
    return 200
