# import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from PIL import Image


class Codephil:

    opacity = 20
    url = "https://codephil.org/"

    def __init__(self) -> None:
        pass

    def download_img(self, link, path):
        try:
            resp = requests.get(link, stream=True)
            resp.raw.decode_content = True
            # save image
            with open(path, "wb") as f:
                shutil.copyfileobj(resp.raw, f)

            img = Image.open(path)
            img.putalpha(self.opacity)
            re_path = "".join(path.split(".")[:-1]) + ".png"
            img.save(re_path, "png")
            return re_path
        except:  # noqa
            return False

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        article_tag_list = soup.find_all("li", attrs={"class": "p-postList__item"})
        link_list = [x.find("a")["href"] for x in article_tag_list]
        result = []
        for link in link_list:
            resp = requests.get(link)
            soup = BeautifulSoup(resp.text, features="html.parser")

            article = {
                "title": None,
                "link": None,
                "top_img_link": None,
                "top_img_path": None,
                "top_content": None,
                "chapter": [],
                # {"category": "chapter", "name": "asdf", "content": "asdf3e", "img_link": "", "img_path": ""}
            }

            article = []

            top = {}
            # title
            top["category"] = "top"
            top["name"] = soup.find("h1").text
            top["link"] = link
            dir_path = f"img/{top['name']}"
            Path(dir_path).mkdir(parents=True, exist_ok=True)

            # top image link
            try:
                top["img_link"] = soup.find(
                    "img", attrs={"class": "p-articleThumb__img"}
                )["data-src"]
                top["img_path"] = dir_path + "/" + top["img_link"].split("/")[-1]
                _img_path = self.download_img(top["img_link"], top["img_path"])
                if not _img_path:
                    top["img_path"] = None
                else:
                    top["img_path"] = _img_path

            except:  # noqa
                top["img_link"] = None
                top["img_path"] = None

            swell_tag = soup.find_all("div", attrs={"class": "swell-block-balloon"})
            [x.decompose() for x in swell_tag]

            post_content_tag = soup.find("div", attrs={"class": "post_content"})

            p_h2_h3_tag = post_content_tag.find_all(["p", "h2", "h3", "img"])

            content = ""
            top_flag = True
            img_flag = True
            for tag in p_h2_h3_tag:
                if not tag.text.strip() == "":
                    content += tag.text.strip() + "\n"
                if tag.name == "img" and img_flag:
                    img_link = tag["src"]
                    if "http" not in img_link:
                        img_link = tag["data-src"]
                    img_path = dir_path + "/" + img_link.split("/")[-1]
                    img_path = self.download_img(img_link, img_path)
                    if not img_path:
                        img_path = None
                    img_flag = False
                if tag.name == "h2":
                    if top_flag:
                        top["content"] = content
                        article.append(top)
                        top_flag = False
                    else:
                        article.append(
                            {
                                "category": "chapter",
                                "name": tag.text,
                                "content": content,
                                "img_link": img_link,
                                "img_path": img_path,
                            }
                        )
                    content = ""
                    img_flag = True
                if tag.name == "h3":
                    article.append(
                        {
                            "category": "section",
                            "name": tag.text,
                            "content": content,
                            "img_link": img_link,
                            "img_path": img_path,
                        }
                    )
                    img_flag = True
                    content = ""
            result.append(article)

            return result
