# import re

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
        result = []
        for link in link_list:
            resp = requests.get(link)
            soup = BeautifulSoup(resp.text, features="html.parser")
            html_content = soup.text
            chapter_tag_list = soup.find_all("div", attrs={"class": "post_content"})[
                0
            ].find_all("h2")
            chapter_list = [
                {"category": "chapter", "content": x.text.strip()}
                for x in chapter_tag_list
            ]
            section_tag_list = soup.find_all("div", attrs={"class": "post_content"})[
                0
            ].find_all("h3")
            section_list = [
                {"category": "section", "content": x.text.strip()}
                for x in section_tag_list
            ]
            for idx, item in enumerate(chapter_list):
                index = html_content.index(item["content"])
                chapter_list[idx]["index"] = index
            for idx, item in enumerate(section_list):
                index = html_content.index(item["content"])
                section_list[idx]["index"] = index

            temp_list = chapter_list + section_list
            index_list = [x["index"] for x in temp_list]
            index_list = sorted(index_list)
            sorted_list = []
            for idx in index_list:
                temp = [x for x in temp_list if x["index"] == idx][0]
                sorted_list.append(temp)
            result.append(sorted_list)

        return link_list
