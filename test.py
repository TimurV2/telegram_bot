import io
path = r'C:\\Users\\1\\PycharmProjects\\telegram_bot\\contacts.txt'
with io.open(path, encoding='utf-8') as file:
    text = file.read()
    print(text)