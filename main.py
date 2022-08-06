import telebot
from telebot import types
import io
import csv


# TODO: - add config to gide token and other info
bot = telebot.TeleBot('5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E')  # Создаем "bot" передаём в него токен бота в TG
admins = [993945655, 1210574996]  # будущий лист админов

# TODO: - change buttons & start command

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Ссылки", "Контакты", "init", "Оставить отзыв", "help", "Уведомить всех"]
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Вот что, я могу сделать:\n'
                                      '<b>Если вам пока не известно, что могут те или иные кнопки, нажмите help</b>',
                                      parse_mode='html', reply_markup=keyboard)


from users_hub import add_user
@bot.message_handler(func=lambda message: message.text == "init")  # инициализируем юзера
def init(message):
    try:
        id = message.from_user.id
        f_name = message.from_user.first_name
        l_name = message.from_user.last_name
        user_name = message.from_user.username
        add_user(id, f_name, l_name, user_name)
        bot.send_message(message.chat.id, 'Поздравляшки! Теперь вы член 8==D')
    except Exception as e:
        bot.send_message(admins[0], str(e))


@bot.message_handler(func=lambda message: message.text == "Оставить отзыв")  # отправка сообщения от пользователя админу
def feedback(message):
    sent = bot.send_message(message.chat.id,
                            'Оставьте свой <u>отзыв / пожелания</u> в следующем сообщении, '
                            'оно будет переслано создателю сего бота.',
                            parse_mode='html')
    bot.register_next_step_handler(sent, frw_msg)
def frw_msg(message):
    if (message.chat.id != 993945655) and (message.text[0] != '/'):
        bot.forward_message(993945655, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено. Спасибо за обратную связь!')


@bot.message_handler(func=lambda message: message.text == "Контакты")  # получение списка контаков по команде /contacts
def contacts(message):
    path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
    with io.open(path, encoding='utf-8') as file:
        text = file.read()
        bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text == "help")  # вывод лога команд
def help(message):
    bot.send_message(message.chat.id, 'Лог команд:\n'
                                      'Контакты - для получения списка контактов преподов\n'
                                      'Оставить отзыв - для отправки отзыва / предложений / сообщения админу\n'
                                      '/start - для вызова меню\n'
                                      'Ссылки - ссылки с важными материалами\n'
                                      'Уведомить всех - для рассылки сообщения всем участникам бота; NB: Пересылается только текст\n'
                                      'init - Платная подписка на рассылки, в базе будет сохранен ваш id, имя, фамилия и username')
    if message.chat.id in admins:
        bot.send_message(message.chat.id, 'Лог команд для избранных:\n'
                                          '/linkpush - для сохранения ссылки в боте\n'
                                          '///позже может появятся ещё///')



from links_funcs import find_url, write_link
@bot.message_handler(commands=['linkpush'])  # пуш ссылки по команде /linkpush
def link_push(message):
    sent = bot.send_message(message.chat.id, 'В <u>одном сообщении</u> введите ссылку и затем её описание', parse_mode='html')
    bot.register_next_step_handler(sent, find_url)


@bot.message_handler(func=lambda message: message.text == "Ссылки")  # получение ссылок по команде /links
def links(message):
    links_msg = write_link()
    bot.send_message(message.chat.id, links_msg)


from users_hub import sent_notify
@bot.message_handler(func=lambda message: message.text == "Уведомить всех")
def notify(message):
    sent = bot.send_message(message.chat.id, '<u>Следующее ваше сообщение</u> будет отправлено всем остальным членам клуба гачи',
                     parse_mode='html')
    bot.register_next_step_handler(sent, sent_notify)



bot.polling(none_stop=True)  # Задаём вечное время работы боту
