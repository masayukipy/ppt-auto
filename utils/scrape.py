import re

import requests
from bs4 import BeautifulSoup


class Codephil:

    url = "https://codephil.org/"

    def __init__(self) -> None:
        pass

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        article_tag_list = soup.find_all("li", attrs={"class": "p-postList__item"})
        link_list = [x.find("a")["href"] for x in article_tag_list]
        for link in link_list:
            resp = requests.get(link)
            soup = BeautifulSoup(resp.text, features="html.parser")
            h1 = soup.find("h1", attrs={"class": "c-postTitle__ttl"}).text
            print(h1)

        return link_list
