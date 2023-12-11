import telebot, buttons
import requests, json
from bs4 import BeautifulSoup


# Капитал банк Узбекистана
based_url = "https://kapitalbank.uz/ru/services/exchange-rates/"
response = requests.get(based_url)
soup = BeautifulSoup(response.text, 'html.parser')

# euro
eur = soup.select('div[class="item item-eur"] div[class="item-picture"]')[0].text.strip()
eur_cost_buy = soup.select('div[class="item item-eur"] div[class="item-rate item-rate-buy"] span[class="item-value"]')[0].text.strip()
eur_cost_sale = soup.select('div[class="item item-eur"] div[class="item-rate item-rate-sale"] span[class="item-value"]')[0].text.strip()

# usd
usd = soup.select('div[class="item item-usd"] div[class="item-picture"]')[0].text.strip()
usd_cost_buy = soup.select('div[class="item item-usd"] div[class="item-rate item-rate-buy"] span[class="item-value"]')[0].text.strip()
usd_cost_sale = soup.select('div[class="item item-usd"] div[class="item-rate item-rate-sale"] span[class="item-value"]')[0].text.strip()

# rub
rub = soup.select('div[class="item item-rub"] div[class="item-picture"]')[0].text.strip()
rub_cost_buy = soup.select('div[class="item item-rub"] div[class="item-rate item-rate-buy"] span[class="item-value"]')[0].text.strip()
rub_cost_sale = soup.select('div[class="item item-rub"] div[class="item-rate item-rate-sale"] span[class="item-value"]')[0].text.strip()

bot = telebot.TeleBot('6332021295:AAEUsjuGfXt-ucLhLElix9zKQskb3FCX_N8')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Добро пожаловать в Конвертер валют!')
    bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())


@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text.lower() == '€ евро':
        bot.send_message(message.from_user.id, f'<b>Выберите Покупка или Продажа?</b>\n\n<i>Цена покупки евро банком:</i>  <b>{eur_cost_buy};</b>\n<i>Цена продажи евро банком:</i> <b>{eur_cost_sale};</b>', parse_mode='HTML', reply_markup=buttons.choice_buy_sale())
        bot.register_next_step_handler(message, buy_or_sale_euro)
    elif message.text.lower() == '$ доллар':
        bot.send_message(message.from_user.id, f'<b>Выберите Покупка или Продажа?</b>\n\n<i>Цена покупки доллара банком:</i>  <b>{usd_cost_buy};</b>\n<i>Цена продажи доллара банком:</i> <b>{usd_cost_sale};</b>', parse_mode='HTML', reply_markup=buttons.choice_buy_sale())
        bot.register_next_step_handler(message, buy_or_sale_usd)
    elif message.text.lower() == '₽ рубль':
        bot.send_message(message.from_user.id, f'<b>Выберите Покупка или Продажа?</b>\n\n<i>Цена покупки рубля банком:</i>  <b>{rub_cost_buy};</b>\n<i>Цена продажи рубля банком:</i> <b>{rub_cost_sale};</b>',parse_mode='HTML', reply_markup=buttons.choice_buy_sale())
        bot.register_next_step_handler(message, buy_or_sale_rub)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял')


def buy_or_sale_euro(message):
    if message.text.lower() == 'покупка':
        bot.send_message(message.from_user.id, 'Введите сумму в суммах!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, buy_euro)
    elif message.text.lower() == 'продажа':
        bot.send_message(message.from_user.id, 'Введите сумму в евро!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, sale_euro)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял тут')


def buy_euro(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) / float(eur_cost_sale), 1)} {eur}</b> \n\n<i>Цена покупки евро Вами: {eur_cost_sale};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, buy_euro)


def sale_euro(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) * float(eur_cost_buy), 1)} сум</b> \n\n<i>Цена продажи евро Вами: {eur_cost_buy};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, sale_euro)


#usd
def buy_or_sale_usd(message):
    if message.text.lower() == 'покупка':
        bot.send_message(message.from_user.id, 'Введите сумму в суммах!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, buy_usd)
    elif message.text.lower() == 'продажа':
        bot.send_message(message.from_user.id, 'Введите сумму в долларах!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, sale_usd)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял тут')


def buy_usd(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) / float(usd_cost_sale), 1)} {usd}</b>\n\n<i>Цена покупки доллара Вами: {usd_cost_sale};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, buy_usd)


def sale_usd(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) * float(usd_cost_buy), 1)} сум </b> \n\n<i>Цена продажи доллара Вами: {usd_cost_buy};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, sale_usd)


#rub
def buy_or_sale_rub(message):
    if message.text.lower() == 'покупка':
        bot.send_message(message.from_user.id, 'Введите сумму в суммах?', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, buy_rub)
    elif message.text.lower() == 'продажа':
        bot.send_message(message.from_user.id, 'Введите сумму в рублях?', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, sale_rub)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял тут')

def buy_rub(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) / float(rub_cost_sale), 1)} {rub}</b>\n\n<i>Цена покупки рубля Вами: {rub_cost_sale};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, buy_rub)

def sale_rub(message):
    try:
        bot.send_message(message.from_user.id, f'🔶 <b>Конвертация Вашей суммы ровна: {round((int(message.text)) * float(rub_cost_buy), 1)} сум</b> \n\n<i>Цена продажи рубля Вами: {rub_cost_buy};</i>',
                         parse_mode='HTML',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}! Выберите валюту для обмена', reply_markup=buttons.choice_buttons())
    except ValueError:
        bot.send_message(message.from_user.id, 'Я вас не понял, Введите пожалуйста сумму в цифрах!')
        bot.register_next_step_handler(message, sale_rub)


bot.polling(non_stop=True)