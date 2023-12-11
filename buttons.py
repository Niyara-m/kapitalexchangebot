from telebot import types

def choice_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    euro = types.KeyboardButton('€ евро')
    dollar = types.KeyboardButton('$ доллар')
    ruble = types.KeyboardButton('₽ рубль')

    kb.add(euro, dollar, ruble)
    return kb

def choice_buy_sale():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buy = types.KeyboardButton('покупка')
    sale = types.KeyboardButton('продажа')

    kb.add(buy, sale)
    return kb