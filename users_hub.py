import csv
import telebot

bot = telebot.TeleBot('5444360230:AAGk1s7gRrfW87b0MnCuMe5q974Hz1Gke7E')

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
            if str(avoid_id) not in row['ID']:
                curr_id = int(row['ID'])
                bot.send_message(curr_id, f'<u>Это сообщение было отправлено от пользователя '
                                          f'@{message.from_user.username}\n</u>' + msg, parse_mode='html')