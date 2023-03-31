import collections  # noqa
import collections.abc  # noqa

from pptx import Presentation

from utils.scrape import Codephil

# prs = Presentation()
# title_slide_layout = prs.slide_layouts[0]
# slide = prs.slides.add_slide(title_slide_layout)
# title = slide.shapes.title
# subtitle = slide.placeholders[1]

# title.text = "Hello, World!"
# subtitle.text = "python-pptx was here!"

# prs.save("test.pptx")

link_list = Codephil().run()
