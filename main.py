import telebot
import uvicorn
import os

import statistics_bot.handlers as handlers
import statistics_bot.set_handlers as set
import statistics_bot.calculators as cls
import statistics_bot.main as main

from statistics_bot.models import Base, User
from statistics_bot.database import engine, session


from functools import wraps


# Initialize bot, app , token
bot, app, TOKEN = main.bot, main.app, main.TOKEN

# Create all tables
Base.metadata.create_all(engine)


def register_required(f):
    @wraps(f)
    def decorated(message, *args, **kwargs):
        user = session.query(User).filter_by(chat_id=message.chat.id).first()

        if user == None:
            bot.reply_to(message, 'Please send /start to register your profile to database')
        else:
            f(message)
    
    return decorated


@bot.message_handler(commands=['start'])
def start_handler(message):
    return handlers.start(bot, message)


@bot.message_handler(commands=['help'])
@register_required
def help_handler(message):
   return handlers.help(bot, message)


@bot.message_handler(commands=['plot'])
@register_required
def plot_handler(message):
   return handlers.plot(bot, message)


@bot.message_handler(commands=['digits'])
@register_required
def digits_handler(message):
   return handlers.digits(bot, message)


@bot.message_handler(commands=['alpha'])
@register_required
def alpha_handler(message):
    return handlers.alpha(bot, message)


@bot.message_handler(regexp='(^/d(1[0-9]|[1-9])$)')
@register_required
def set_digits(message):
    return set.digits(bot, message)
    

@bot.message_handler(regexp='(^/a(0*[.][0-9]*[1-9]$)$)')
@register_required
def set_alpha(message):
    return set.alpha(bot, message)


@bot.message_handler(func=lambda msg: msg.text == 'Switch')
@bot.message_handler(func=lambda msg: msg.text == 'Cancel')
@register_required
def set_plot_mode(message):
    return set.plot(bot, message)


@bot.message_handler(regexp='/Admin .')
@register_required
def set_admin_handler(message):
    return set.admin(bot, message)


@bot.message_handler(regexp='(^ni? [+-]?([0-9]*[.])?[0-9]+$)|(^ti? [+-]?([0-9]*[.])?[0-9]+ [1-9][0-9]*$)')
@register_required
def distribution_calculator(message):
    return cls.distribution(bot, message)


@bot.message_handler(regexp='^(n|t)test [+-]?([0-9]*[.])?[0-9]* [+-]?([0-9]*[.])?[0-9]* ([0-9]*[.])?[0-9]* ([1-9][0-9]*) [<=>]$')
@register_required
def tests_calculator(message):
    return cls.tests(bot, message)


@bot.message_handler(regexp='^v( ([0-9]*[.])?[0-9]+)+$')
@register_required
def variance_calculator(message):
    return cls.variance(bot, message)


@bot.message_handler(func=lambda msg: True, content_types=['text'])
@register_required
def input_handler(message):
    return handlers.input(bot, message)
