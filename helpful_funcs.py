from telebot.types import ReplyKeyboardMarkup

def gen_markup():
    keyboard = ReplyKeyboardMarkup()
    buttons = ["Ссылки", "Контакты", "Инициализация", "Оставить отзыв", "Помощь", "Уведомить всех", "Гороскоп"]
    keyboard.resize_keyboard = True
    keyboard.add(*buttons)
    return keyboard

def exit_markup():
    keyboard = ReplyKeyboardMarkup()
    button = "Отменить"
    keyboard.resize_keyboard = True
    keyboard.add(button)
    return keyboard