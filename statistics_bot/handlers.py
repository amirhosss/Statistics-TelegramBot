from .database import session
from .models import User
from telebot import types

# Create handlers for bot commands
def start(bot, message):
    users = session.query(User).filter_by(chat_id=message.chat.id).first()
    
    if users == None:
        user = User(chat_id=message.chat.id, username=message.chat.username)
        session.add(user)
        session.commit()
    
    bot.reply_to(message,
                 'Please send a massage,\nsend /help to see the format')


def help(bot, message):
    bot.reply_to(message, 
                   '&#x1F4C9 Variance\ne.g. (X&#x2080=5, X&#x2081=42 ..., X&#x2099=70):\n<b>v 5 42 ... 70</b>\n\n'
                 + '&#x1F4CA Normal. Inverse survival function\ne.g. (&#x03b1 = 0.05):\n<b>n.isf 0.05</b>\n'
                 + '&#x1F4CA Normal. Survival function\ne.g. (x = 1):\n<b>n.sf 1</b>\n' 
                 + '&#x1F4CA t-student. Inverse survival function\ne.g. (&#x3b1 = 0.05, &#x3bd = 9):\n<b>t.isf 0.05 9</b>\n'
                 + '&#x1F4CA t-student. Survival function\ne.g. (x = 1, v = 9):\n<b>t.sf 1 9</b>\n\n' 
                 + '&#x1F4C8 Normal test\ne.g. (X&#x305 = 14, &#x3BC = 13, &#x3C3 = 2, n = 10, (H&#x2081: &#x3BC&gt&#x3BC&#x2080) = &gt):\n<b>ntest 14 13 2 10 &gt</b>\n'
                 + '&#x1F4C8 t test\ne.g. (X&#x305 = 14, &#x3BC = 13, S = 2, n = 10, (H&#x2081: &#x3BC&lt&#x3BC &#x2080) = &lt):\n<b>ttest 14 13 2 10 &lt</b>\n\n'
                 + '&#x1F527 Send /plot to change the plot mode\n(default: on)\n' 
                 + '&#x1F527 Send /alpha to set the alpha_value for hypothesis tests\n(default: 0.05)\n' 
                 + '&#x1F527 Send /digits to set digits for\nanswers (default: 6)', 
                    parse_mode='HTML')


def plot(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
   
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton('Switch')
    btn_2 = types.KeyboardButton('Cancel')
    markup.row(btn_1, btn_2)
    
    
    condition = {True: 'On', False: 'Off'}
    bot.reply_to(message, f'Plot mode is {condition[user.plot_mode]}\n' 
    + 'Choose Switch, to switch the mode or Cancel to leave it alone', reply_markup=markup)


def digits(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    bot.reply_to(message, f'\U0001F4CF Digits: {user.digits}\n' 
    + 'To change it please send command in below format:\n' 
    + '\U0001F4CC /d<Your preffered number>\ndigits must above 0 and below 20\n' 
    + 'e.g. /d9')


def alpha(bot, message):
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    bot.reply_to(message, f'\U0001F4CF Alpha: {user.alpha}\n' 
    + 'To change it please send command in below format:\n' 
    + '\U0001F4CC /a<Your preffered alpha>\nalpha must above 0 and below 1\n' 
    + 'e.g. /a0.5')


def input(bot, message):
    bot.reply_to(message, 'Wrong input')


