# import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class Codephil:

    url = "https://codephil.org/"

    def __init__(self) -> None:
        pass

    def download_img(self, link, path):
        resp = requests.get(link, stream=True)
        resp.raw.decode_content = True
        # save image
        with open(path, "wb") as f:
            shutil.copyfileobj(resp.raw, f)

    def run(self):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        article_tag_list = soup.find_all("li", attrs={"class": "p-postList__item"})
        link_list = [x.find("a")["href"] for x in article_tag_list]
        result = []
        for link in link_list:
            resp = requests.get(link)
            soup = BeautifulSoup(resp.text, features="html.parser")
            html_content = str(soup)

            article = {
                "title": None,
                "link": None,
                "top_img_link": None,
                "top_img_path": None,
                "top_content": None,
                "chapter": [],  # {"category": "chapter", "name": "asdf", "content": "asdf3e", "img_link": "", "img_path": ""}
            }

            # title
            article["title"] = soup.find("h1").text
            article["link"] = link
            dir_path = f"img/{article['title']}"
            Path(dir_path).mkdir(parents=True, exist_ok=True)

            # top image link
            try:
                article["top_img_link"] = soup.find(
                    "img", attrs={"class": "p-articleThumb__img"}
                )["data-src"]
                article["top_img_path"] = (
                    dir_path + "/" + article["top_img_link"].split("/")[-1]
                )
                self.download_img(article["top_img_link"], article["top_img_path"])
            except:
                article["top_img_link"] = None
                article["top_img_path"] = None

            swell_tag = soup.find_all("div", attrs={"class": "swell-block-balloon"})
            [x.decompose() for x in swell_tag]

            post_content_tag = soup.find("div", attrs={"class": "post_content"})

            p_h2_h3_tag = post_content_tag.find_all(["p", "h2", "h3", "img"])

            content = ""
            top_flag = True
            img_flag = True
            for tag in p_h2_h3_tag:
                content += tag.text + "\n"
                if tag.name == "img" and img_flag:
                    img_link = tag["src"]
                    if not "http" in img_link:
                        img_link = tag["data-src"]
                    img_path = dir_path + "/" + img_link.split("/")[-1]
                    self.download_img(img_link, img_path)
                    img_flag = False
                if tag.name == "h2":
                    if top_flag:
                        article["top_content"] = content
                        top_flag = False
                    else:
                        article["chapter"].append(
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
                    article["chapter"].append(
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

            # # chapter tag list
            # chapter_tag_list = soup.find_all("div", attrs={"class": "post_content"})[
            #     0
            # ].find_all("h2")
            # chapter_list = [
            #     {"category": "chapter", "content": x.text.strip()}
            #     for x in chapter_tag_list
            # ]

            # # section tag list
            # section_tag_list = soup.find_all("div", attrs={"class": "post_content"})[
            #     0
            # ].find_all("h3")
            # section_list = [
            #     {"category": "section", "content": x.text.strip()}
            #     for x in section_tag_list
            # ]

            # # imgae tag list
            # img_tag_list = soup.find_all(attrs={"class": "size-full"})
            # img_tag_list = set(img_tag_list)
            # img_list = []
            # for tag in img_tag_list:
            #     if tag.name == "figure":
            #         img_list.append({
            #             "category": "img",
            #             "content": tag.img["data-src"]
            #         })
            #     else:
            #         try:
            #             img_list.append({
            #                 "category": "img",
            #                 "content": tag["data-src"]
            #             })
            #         except:
            #             img_list.append({
            #                 "category": "img",
            #                 "content": tag["src"]
            #             })

            # for idx, item in enumerate(chapter_list):
            #     index = html_content.index(item["content"])
            #     chapter_list[idx]["index"] = index
            # for idx, item in enumerate(section_list):
            #     index = html_content.index(item["content"])
            #     section_list[idx]["index"] = index
            # for idx, item in enumerate(img_list):
            #     index = html_content.index(item["content"])
            #     img_list[idx]["index"] = index
            #     path = Path(f"img/{title}").mkdir(parents=True, exist_ok=True)

            #     url = item["content"]

            #     item["content"] = path

            # temp_list = chapter_list + section_list + img_list
            # index_list = [x["index"] for x in temp_list]
            # index_list = sorted(index_list)
            # sorted_list = []
            # for idx in index_list:
            #     temp = [x for x in temp_list if x["index"] == idx][0]
            #     sorted_list.append(temp)
            # result.append({"title": title, "img_link": top_img_link, "url": link, "content": sorted_list})

        return result
