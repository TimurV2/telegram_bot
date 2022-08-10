import csv
from urlextract import URLExtract


def find_url(message):

    try:
        string = message.text
        extractor = URLExtract()
        urls = extractor.find_urls(string)
        with open('links_hub.csv', 'a+', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([str(urls[0]), string.replace(str(urls[0]), '')])
    except Exception as e:
        pass


def write_link():
    with open('links_hub.csv', 'r') as file:
        reader = csv.reader(file)
        text = ''
        for line in file:
            text += line
        text = text.replace(',', '')
        if text == '':
            text = 'Извините, тут пока нет ни одной ссылки'
        return text

