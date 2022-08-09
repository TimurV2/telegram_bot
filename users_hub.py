import csv
import telebot
import os

TELEGRAM_TOKEN = str(os.environ['bot_token'])

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def add_user(user_id, first_name, last_name, user_name):
    attend = False
    user_info = [user_id, first_name, last_name, user_name]
    with open('users_hub.csv', 'a', newline='', encoding='utf-8') as writable_file:
        with open('users_hub.csv', 'r') as readable_file:
            reader = csv.DictReader(readable_file)
            for row in reader:
                if str(user_id) in row['ID']:
                    attend = True
                    readable_file.close()
                    break
        if not attend:
            writer = csv.writer(writable_file)
            writer.writerow(user_info)
            writable_file.close()

def sent_notify(message):
    msg = message.text
    avoid_id = message.chat.id
    with open('users_hub.csv', 'r') as readable_file:
        reader = csv.DictReader(readable_file)
        for row in reader:
            if (str(avoid_id) not in row['ID']) and (message.text not in ["Ссылки", "Контакты", "Инициализация", "Оставить отзыв", "Помощь", "Уведомить всех"]):
                curr_id = int(row['ID'])
                bot.send_message(curr_id, f'<u>Общее уведомление от пользователя - '
                                          f'@{message.from_user.username}\n</u>' + msg, parse_mode='html')


def frw_msg(message):
    if (message.chat.id != 993945655) and (message.text[0] != '/'):
        bot.forward_message(993945655, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Ваше сообщение было отправлено. Спасибо за обратную связь!')