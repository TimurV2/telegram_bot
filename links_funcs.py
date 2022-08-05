import re
import csv
from urlextract import URLExtract

def find_url(message):
    # regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    # url = re.findall(regex, string)
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
            text = 'Извините, тут пока нет ниодной ссылки'
        return text

