import collections  # noqa
import collections.abc  # noqa
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pptx import Presentation

from utils.drive import Drive
from utils.ppt import create_slide
from utils.scrape import Codephil

load_dotenv()
Path("ppt").mkdir(parents=True, exist_ok=True)
root_id = os.getenv("ROOTID")
drive = Drive()


def all():
    article_list = Codephil().all_run()
    for article in article_list:
        prs = Presentation()
        for chapter in article:
            create_slide(prs, chapter)
        path = f'ppt/{article[0]["name"]}.pptx'
        prs.save(path)
        drive.upload_file(root_id, path)


def each(link):
    article = Codephil().req_article(link)
    prs = Presentation()
    for chpater in article:
        create_slide(prs, chpater)
    path = f'ppt/{article[0]["name"]}.pptx'
    prs.save(path)
    drive.upload_file(root_id, path)


# each("https://codephil.org/fxauto/")
# all()
if sys.argv[1] == "all":
    all()
else:
    text = input("Enter URL: ")
    each(text)
