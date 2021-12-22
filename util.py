import requests
from lxml import html

def make_num(string):
    nb=""
    for l in string:
        if l.isnumeric():
            nb += l
    try:
        return int(nb)
    except:
        return 0

def get_tree(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    return tree
