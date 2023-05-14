import telebot
from currency_converter import CurrencyConverter
from telebot import types
bot = telebot.TeleBot('6089956846:AAGCu-TuqsFvxbm61qnZz-pA8AKjK_zjaGo')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, enter amount')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'format is not supported, try to type right currency format')
        bot.register_next_step_handler(message, summa)
        return
    
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/SUD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('other', callback_data='else')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'choose currency', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'currency value must be greater than 0, try to type right currency format')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'The result is: {round(res,2)}. you can enter another currency again')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'enter currency type')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'The result is: {round(res,2)}. you can enter another currency again')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Something went wrong. Enter correct currency type')
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)
