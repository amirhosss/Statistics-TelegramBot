import telebot

import config

from fastapi import FastAPI


# Create bot instance
bot = telebot.TeleBot(config.TOKEN, threaded=False)

# Create server
if config.SERVER_MODE == 'production':
    app = FastAPI(docs_url=None, redoc_url=None)

    import statistics_bot.routers.router as router
    app.include_router(router.router)