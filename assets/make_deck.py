"""Build the shareable EnigmiQ CAD and integration overview deck."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


OUT = Path(__file__).with_name("enigmiq-cad-integration-overview.pptx")
DEMO = "https://enigmiq.com/#demos"
NAVY = RGBColor(8, 18, 34)
PANEL = RGBColor(18, 36, 55)
CYAN = RGBColor(113, 219, 240)
WHITE = RGBColor(237, 247, 255)
MUTED = RGBColor(160, 181, 200)


def box(slide, x, y, w, h, color=PANEL):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def words(slide, text, x, y, w, h, size=21, color=WHITE, bold=False, link=None):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.02)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    paragraph = frame.paragraphs[0]
    paragraph.alignment = PP_ALIGN.LEFT
    run = paragraph.add_run()
    run.text = text
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    if link:
        run.hyperlink.address = link
    return shape


def base(prs, title, number):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY
    words(slide, "ENIGMIQ TECHNOLOGIES", .65, .31, 5, .35, 11, CYAN, True)
    words(slide, title, .65, .9, 11.6, .75, 32, WHITE, True)
    words(slide, f"{number:02d}  |  enquiry@enigmiq.com  |  enigmiq.com", .65, 7.1, 12, .25, 10, MUTED)
    return slide


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

slide = base(prs, "Engineering CAD with a useful AI assistant", 1)
words(slide, "A short overview for machine builders and mechanical design teams", .68, 1.86, 10.8, .55, 22, MUTED)
box(slide, .67, 2.78, 12, 3.15)
words(slide, "EnigmiQ CAD", 1.05, 3.1, 4.7, .5, 25, CYAN, True)
words(slide, "Create and revise native, editable CAD from a reviewed description.", 1.05, 3.7, 10.8, 1, 25)
words(slide, "A separate custom engagement can explore a copilot inside the software your team already uses.", 1.05, 4.92, 10.8, .72, 20, MUTED)

slide = base(prs, "A CAD model engineers can keep editing", 2)
steps = [
    ("01", "Describe", "Start with a part brief or reference image."),
    ("02", "Review", "Approve dimensions before the model is built."),
    ("03", "Build", "Get constrained sketches and native features."),
    ("04", "Revise", "Change named parameters and update drawings."),
]
for idx, (number, title, detail) in enumerate(steps):
    x = .67 + idx * 3.08
    box(slide, x, 2.25, 2.88, 3.25)
    words(slide, number, x + .24, 2.53, 1, .35, 14, CYAN, True)
    words(slide, title, x + .24, 3.03, 2.4, .48, 22, WHITE, True)
    words(slide, detail, x + .24, 3.76, 2.36, 1.2, 17, MUTED)
words(slide, "The website shows STEP recovery, linked drawings, assembly motion, and the parameter graph.", .67, 5.94, 11.8, .46, 16, MUTED)

slide = base(prs, "Four short CAD films", 3)
films = [
    ("01  Idea to editable V8 assembly", "Native parts and solver-driven motion", "1:22"),
    ("02  Reference image to drawing", "Reviewed dimensions and linked PDF drawing", "2:21"),
    ("03  STEP to editable features", "Recovered sketches, features, and parameters", "1:43"),
    ("04  Parameter graph and revisions", "Named dimensions with Undo and Redo", "1:18"),
]
for idx, (title, detail, length) in enumerate(films):
    y = 2.02 + idx * 1.06
    box(slide, .67, y, 12, .89)
    words(slide, title, .94, y + .13, 6.9, .34, 19, WHITE, True, DEMO)
    words(slide, detail, 8.08, y + .15, 3.62, .45, 13, MUTED)
    words(slide, length, 11.87, y + .17, .47, .31, 12, CYAN)
words(slide, "Watch all films at enigmiq.com/#demos", .67, 6.48, 7, .35, 17, CYAN, True, DEMO)

slide = base(prs, "A copilot scoped to your current tools", 4)
words(slide, "The integration offer begins with a discovery call and a feasibility check of the software, files, and workflow your engineers use.", .67, 1.86, 11.9, 1.05, 23)
box(slide, .67, 3.15, 5.77, 2.4)
box(slide, 6.64, 3.15, 6.03, 2.4)
words(slide, "Possible first pilot", .97, 3.42, 5.1, .42, 21, CYAN, True)
words(slide, "One repetitive part family, a drawing revision, or a review step.", .97, 4.09, 5.05, 1, 19)
words(slide, "What we would agree first", 6.94, 3.42, 5.2, .42, 21, CYAN, True)
words(slide, "Supported interface, example files, approval rules, and measurable acceptance criteria.", 6.94, 4.09, 5.2, 1, 19)
words(slide, "Integration feasibility depends on the customer's software and permissions.", .67, 6.1, 11.6, .44, 16, MUTED)

slide = base(prs, "Choose one workflow worth testing", 5)
words(slide, "A useful first conversation identifies the CAD system, the task engineers repeat, and one sample that can be shared safely.", .67, 1.91, 11.5, 1.18, 24)
box(slide, .67, 3.42, 12, 1.59)
words(slide, "Next step", .98, 3.72, 2.2, .38, 17, CYAN, True)
words(slide, "A 20-minute walkthrough and a scoped pilot proposal after technical discovery.", 3.07, 3.67, 8.87, .7, 21)
words(slide, "Full demo library: four CAD films plus the Floorcraft architecture walkthrough", .67, 5.52, 11.8, .43, 16, MUTED, link=DEMO)
words(slide, "enigmiq.com/#demos", .67, 6.05, 6, .39, 19, CYAN, True, DEMO)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print(OUT)