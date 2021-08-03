import scipy.stats as st
import numpy as np

from math import sqrt

from .external_api import chart_api
from .models import User
from .database import session

# Calculate statistics function for user inputs
def distribution(bot, message):
    dist = message.text.lower().split(' ')
    length = len(dist)

    distribution = dist[0]
    dist = [float(_dist) for _dist in dist[1:]]
    dist.insert(0, distribution)

    if distribution == 'n.sf':
        ans = st.norm.sf(float(dist[1]))
        data = [dist[1], st.norm.pdf(dist[1])]

    elif distribution == 'n.isf':
        ans = st.norm.isf(float(dist[1]))
        data = [ans, st.norm.pdf(ans)]

    elif distribution == 't.sf':
        ans = st.t.sf(float(dist[1]), float(dist[2]))
        data = [dist[1], st.t.pdf(dist[1], dist[2])]

    elif distribution == 't.isf':
        ans = st.t.isf(float(dist[1]), float(dist[2]))
        data = [ans, st.t.pdf(ans, dist[2])]
    
    param = 0
    if length == 3:
        param = float(dist[2])
    
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    msg = bot.reply_to(message, f'Answer = {round(ans, user.digits)}' if type(ans) != str else ans)

    user = session.query(User).filter(User.chat_id==message.chat.id).first()
    if user.plot_mode:
        api_data = chart_api(distribution[0], data, param)

        msg_id = bot.reply_to(msg, api_data[1][0])
        if len(api_data) > 1:
            bot.edit_message_text(api_data[1][1], message.chat.id, msg_id.message_id)
        if api_data[0] != None:
            bot.send_photo(message.chat.id, api_data[0])
            bot.delete_message(message.chat.id, msg_id.message_id)


def tests(bot, message):
    method = message.text.lower().split(' ')[0]
    x_bar, mu, sigma_s, n = [float(msg) for msg in message.text.lower().split(' ')[1:-1]]
    alternative = message.text.lower().split(' ')[-1]
    
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    if sigma_s > 0:
        _param = (x_bar-mu)*sqrt(n)/sigma_s

        bot.reply_to(message, f'Param_value = {round(_param, user.digits)}')

        if method == 'ntest':

            if alternative == '<':
                interval = st.norm.isf(user.alpha)
                bot.reply_to(message, f'Interval = ({-interval.round(user.digits)}, \u221E)')

                if _param >= -interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
            elif alternative == '=':
                interval = st.norm.isf((user.alpha)/2)
                bot.reply_to(message, f'Interval = ({round(-interval, user.digits)}, {round(interval, user.digits)})')
                
                if _param >= -interval and _param <= interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
            else:
                interval = st.norm.isf(user.alpha)
                bot.reply_to(message, f'Interval = (-\u221E, {interval.round(user.digits)})')

                if _param <= interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
        else:

            if alternative == '<':
                interval = st.t.isf(user.alpha, n-1)
                bot.reply_to(message, f'Interval = ({-interval.round(user.digits)}, \u221E)')

                if _param >= -interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
            elif alternative == '=':
                interval = st.t.isf((user.alpha)/2, n-1)
                bot.reply_to(message, f'Interval = ({-interval.round(user.digits)}, {interval.round(user.digits)})')

                if _param >= -interval and _param <= interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
            else:
                interval = st.t.isf(user.alpha, n-1)
                bot.reply_to(message, f'Interval = (-\u221E, {interval.round(user.digits)})')

                if _param <= interval:
                    bot.reply_to(message, 'The null hypothesis can be accepted \u2705')
                else:
                    bot.reply_to(message, 'The null hypothesis cannot be accepted \u274C')
    else:
        bot.reply_to(message, '\u03C3 or S cannot be 0')


def variance(bot, message):
    msg = message.text.lower().split(' ')
    
    str_numbers = msg[1:]
    numbers = [float(_num) for _num in str_numbers]

    ans = np.var(numbers)

    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    bot.reply_to(message, f'Answer = {round(ans, user.digits) if type(ans)!=str else ans}')

