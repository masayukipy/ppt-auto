import collections  # noqa
import collections.abc  # noqa

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt

from utils.scrape import Codephil

# prs = Presentation()
# subtitle = slide.placeholders[1]

# title.text = "Hello, World!"
# subtitle.text = "python-pptx was here!"

# prs.save("test.pptx")
font_size = 42


def create_slide(prs, text):
    mul_text = ""
    while True:
        if len(text) > 15:
            mul_text = text[:15] + "\n"
            text = text[15:]
        else:
            mul_text += text
            break

    mul_len = len(mul_text.split("\n"))

    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tx_box = slide.shapes.add_textbox(0, 0, prs.slide_width, Pt(font_size) * mul_len)

    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = mul_text
    p.alignment = PP_ALIGN.CENTER

    font = run.font
    font.name = "MS Mincho"
    font.size = Pt(font_size)
    tx_box.left = int((prs.slide_width - tx_box.width) / 2)
    tx_box.top = int(
        (prs.slide_height - Pt(font_size + 20 + (mul_len - 1) * font_size)) / 2
    )


def all():
    article_list = Codephil().run()
    for article in article_list:
        prs = Presentation()
        create_slide(prs, article["title"])
        for chapter in article["content"]:
            create_slide(prs, chapter["content"])
        prs.save(f'{article["title"]}.pptx')


all()
