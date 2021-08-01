import os
import telebot

from fastapi import FastAPI
from dotenv import load_dotenv


# Get bot token from enviroment configs
load_dotenv()
TOKEN = os.environ.get('TOKEN')

# Create bot instance
bot = telebot.TeleBot(TOKEN, threaded=False)

# Create server
app = FastAPI(docs_url=None, redoc_url=None)

import statistics_bot.routers.router as router

app.include_router(router.router)

