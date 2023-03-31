import collections  # noqa
import collections.abc  # noqa

from pptx import Presentation

from utils.ppt import create_slide
from utils.scrape import Codephil


def all():
    article_list = Codephil().all_run()
    for article in article_list:
        prs = Presentation()
        for chapter in article:
            create_slide(prs, chapter)
        prs.save(f'ppt/{article[0]["name"]}.pptx')


def each(link):
    article = Codephil().req_article(link)
    prs = Presentation()
    for chpater in article:
        create_slide(prs, chpater)
    prs.save(f'ppt/{article[0]["name"]}.pptx')


each("https://codephil.org/fxauto/")
