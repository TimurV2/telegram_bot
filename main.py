import telebot
import io
from telebot import types
from links_funcs import find_url, write_link
from users_hub import add_user, sent_notify, frw_msg, ask_horo
from helpful_funcs import gen_markup
import os
import requests
from bs4 import BeautifulSoup


TELEGRAM_TOKEN = str(os.environ['bot_token'])
urls = {'Овен':'https://horo.mail.ru/prediction/aries/today/',
     'Телец':'https://horo.mail.ru/prediction/taurus/today/',
     'Близнецы':'https://horo.mail.ru/prediction/gemini/today/',
     'Рак':'https://horo.mail.ru/prediction/cancer/today/',
     'Лев':'https://horo.mail.ru/prediction/leo/today/',
     'Дева':'https://horo.mail.ru/prediction/virgo/today/',
     'Весы':'https://horo.mail.ru/prediction/libra/today/',
     'Скорпион':'https://horo.mail.ru/prediction/scorpio/today/',
     'Стрелец':'https://horo.mail.ru/prediction/sagittarius/today/',
     'Козерог':'https://horo.mail.ru/prediction/capricorn/today/',
     'Водолей':'https://horo.mail.ru/prediction/aquarius/today/',
     'Рыбы':'https://horo.mail.ru/prediction/pisces/today/'}
bot = telebot.TeleBot(TELEGRAM_TOKEN)
admins = [993945655, 1210574996]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Вот что, я могу сделать:\n'
                                      '<b>Если вам пока не известно, что могут те или иные кнопки, нажмите "Помощь"</b>',
                     parse_mode='html', reply_markup=gen_markup())


@bot.message_handler(commands=['linkpush'])  # пуш ссылки по команде /linkpush
def link_push(message):
    sent = bot.send_message(message.chat.id, 'В <u>одном сообщении</u> введите ссылку и затем её описание', parse_mode='html')
    bot.register_next_step_handler(sent, find_url)


@bot.message_handler()
def text_message_handler(message):
    match message.text:
        case "Ссылки":
            links_msg = write_link()
            bot.send_message(message.chat.id, links_msg, reply_markup=gen_markup())
        case "Контакты":
            path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
            with io.open(path, encoding='utf-8') as file:
                text = file.read()
                bot.send_message(message.chat.id, text, reply_markup=gen_markup())
        case "Инициализация":
            try:
                id = message.from_user.id
                f_name = message.from_user.first_name
                l_name = message.from_user.last_name
                user_name = message.from_user.username
                add_user(id, f_name, l_name, user_name)
                bot.send_message(message.chat.id, 'Поздравляшки! Теперь вы член 8==D', reply_markup=gen_markup())
            except Exception as e:
                bot.send_message(admins[0], str(e))
        case "Уведомить всех":
            sent = bot.send_message(message.chat.id,
                                    '<u>Следующее ваше сообщение</u> будет отправлено всем остальным членам клуба гачи',
                                    parse_mode='html')
            bot.register_next_step_handler(sent, sent_notify)
        case "Помощь":
            bot.send_message(message.chat.id, 'Лог команд:\n\n'
                                              'Контакты - для получения списка контактов преподов\n\n'
                                              'Оставить отзыв - для отправки отзыва / предложений / сообщения админу\n\n'
                                              '/start - для вызова меню\n\n'
                                              'Ссылки - ссылки с важными материалами\n\n'
                                              'Уведомить всех - для рассылки сообщения всем участникам бота; NB: Пересылается только текст\n\n'
                                              'Инициализация - Платная подписка на рассылки, в базе будет сохранен ваш id, имя, фамилия и username\n\n'
                                              'Гороскоп - если вам захотелось узнать свою судьбу ¯\_(ツ)_/¯\n\n', reply_markup=gen_markup())
            if message.chat.id in admins:
                bot.send_message(message.chat.id, 'Лог команд для избранных:\n\n'
                                                  '/linkpush - для сохранения ссылки в боте\n\n'
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
        url = urls[call.data]
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        prediction = soup.find_all('p')
        prediction[0] = str(prediction[0]).replace('<p>', '').replace('</p>', '')
        prediction[1] = str(prediction[1]).replace('<p>', '').replace('</p>', '')
        bot.send_message(call.message.chat.id,'Ваш гороскоп на сегодня:\n\n' + f'{prediction[0]}\n\n' + f'{prediction[1]}')


bot.polling(none_stop=True)
