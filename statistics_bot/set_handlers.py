from .models import User
from .database import session
from telebot import types

# Get input from bot and do SMTH
def digits(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    digits = message.text.split('/d')[1]
    
    user.digits = digits
    session.commit()

    bot.reply_to(message, f'Digits: {digits}')
    

def alpha(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    
    alpha = message.text.split('/a')[1]
    
    user.alpha = alpha
    session.commit()

    bot.reply_to(message, f'Alpha: {alpha}')


def plot(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    
    markup = types.ReplyKeyboardRemove()

    if message.text == 'Switch':
        user.plot_mode = not user.plot_mode
        session.commit()
        
        condition = {True: 'On', False: 'Off'}
        bot.reply_to(message, f'Plot mode is {condition[user.plot_mode]}', reply_markup=markup)
    else:
        bot.reply_to(message, 'Nothing changed', reply_markup=markup)


def admin(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    if user.chat_id == 529241259:
        user_all = session.query(User).all()

        for user in user_all:
            bot.send_message(user.chat_id, message.text.split('/Admin ')[1])
    else:
        bot.reply_to(message, 'Sorry you are not admin')
