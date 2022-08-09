import telebot
import io
from telebot import types
from links_funcs import find_url, write_link
from users_hub import add_user, sent_notify, frw_msg
import os
import requests
from bs4 import BeautifulSoup
from test import ask_horo

TELEGRAM_TOKEN = str(os.environ['bot_token'])
urls = ['https://horo.mail.ru/prediction/aries/today/',
        'https://horo.mail.ru/prediction/taurus/today/',
        'https://horo.mail.ru/prediction/gemini/today/',
        'https://horo.mail.ru/prediction/cancer/today/',
        'https://horo.mail.ru/prediction/leo/today/',
        'https://horo.mail.ru/prediction/virgo/today/',
        'https://horo.mail.ru/prediction/libra/today/',
        'https://horo.mail.ru/prediction/scorpio/today/',
        'https://horo.mail.ru/prediction/sagittarius/today/',
        'https://horo.mail.ru/prediction/capricorn/today/',
        'https://horo.mail.ru/prediction/aquarius/today/',
        'https://horo.mail.ru/prediction/pisces/today/']
bot = telebot.TeleBot(TELEGRAM_TOKEN)
admins = [993945655, 1210574996]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Ссылки", "Контакты", "Инициализация", "Оставить отзыв", "Помощь", "Уведомить всех", "Гороскоп"]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Вот что, я могу сделать:\n'
                                      '<b>Если вам пока не известно, что могут те или иные кнопки, нажмите help</b>',
                     parse_mode='html', reply_markup=keyboard)


@bot.message_handler(commands=['linkpush'])  # пуш ссылки по команде /linkpush
def link_push(message):
    sent = bot.send_message(message.chat.id, 'В <u>одном сообщении</u> введите ссылку и затем её описание', parse_mode='html')
    bot.register_next_step_handler(sent, find_url)


@bot.message_handler()
def text_message_handler(message):
    match message.text:
        case "Ссылки":
            links_msg = write_link()
            bot.send_message(message.chat.id, links_msg)
        case "Контакты":
            path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
            with io.open(path, encoding='utf-8') as file:
                text = file.read()
                bot.send_message(message.chat.id, text)
        case "Инициализация":
            try:
                id = message.from_user.id
                f_name = message.from_user.first_name
                l_name = message.from_user.last_name
                user_name = message.from_user.username
                add_user(id, f_name, l_name, user_name)
                bot.send_message(message.chat.id, 'Поздравляшки! Теперь вы член 8==D')
            except Exception as e:
                bot.send_message(admins[0], str(e))
        case "Уведомить всех":
            sent = bot.send_message(message.chat.id,
                                    '<u>Следующее ваше сообщение</u> будет отправлено всем остальным членам клуба гачи',
                                    parse_mode='html')
            bot.register_next_step_handler(sent, sent_notify)
        case "Помощь":
            bot.send_message(message.chat.id, 'Лог команд:\n'
                                              'Контакты - для получения списка контактов преподов\n'
                                              'Оставить отзыв - для отправки отзыва / предложений / сообщения админу\n'
                                              '/start - для вызова меню\n'
                                              'Ссылки - ссылки с важными материалами\n'
                                              'Уведомить всех - для рассылки сообщения всем участникам бота; NB: Пересылается только текст\n'
                                              'Инициализация - Платная подписка на рассылки, в базе будет сохранен ваш id, имя, фамилия и username')
            if message.chat.id in admins:
                bot.send_message(message.chat.id, 'Лог команд для избранных:\n'
                                                  '/linkpush - для сохранения ссылки в боте\n'
                                                  '///позже может появятся ещё///')
        case "Оставить отзыв":
            sent = bot.send_message(message.chat.id,
                                    'Оставьте свой <u>отзыв / пожелания</u> в следующем сообщении, '
                                    'оно будет переслано создателю сего бота.',
                                    parse_mode='html')
            bot.register_next_step_handler(sent, frw_msg)
        case "Гороскоп":
            ask_horo(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        match call.data:
            case "Овен":
                url = urls[0]
            case "Телец":
                url = urls[1]
            case "Близнецы":
                url = urls[2]
            case "Рак":
                url = urls[3]
            case "Лев":
                url = urls[4]
            case "Дева":
                url = urls[5]
            case "Весы":
                url = urls[6]
            case "Скорпион":
                url = urls[7]
            case "Стрелец":
                url = urls[8]
            case "Козерог":
                url = urls[9]
            case "Водолей":
                url = urls[10]
            case "Рыбы":
                url = urls[11]

        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        prediction = soup.find_all('p')
        prediction[0] = str(prediction[0]).replace('<p>', '').replace('</p>', '')
        prediction[1] = str(prediction[1]).replace('<p>', '').replace('</p>', '')
        bot.send_message(call.message.chat.id, f'{prediction[0]}\n\n' + f'{prediction[1]}')


bot.polling(none_stop=True)
