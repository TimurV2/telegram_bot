import re
import pandas as pd
import csv

def find_url(message):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    string = message.text
    url = re.findall(regex, string)
    with open('link_hub.csv', 'a') as file:
        pass
        # TODO: добавить запись в csv файл
    # return string.replace(url[0][0], ''), url[0][0]

