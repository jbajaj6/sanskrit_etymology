#!/usr/bin/env /opt/homebrew/bin/python3.11
"""
Generate a PowerPoint (.pptx) presentation from a structured slide spec.

Usage:
    python3.11 src/utils/generate_pptx.py <input_yaml> <output_pptx>

The input YAML should have the following structure:

    title: "Presentation Title"
    subtitle: "Subtitle"
    author: "Author Name"
    date: "2026-04-09"

    theme:
      font_heading: "Helvetica"
      font_body: "Helvetica"
      color_heading: "1a1a2e"    # hex, no #
      color_accent: "c0392b"
      color_body: "2c3e50"
      color_bg: "ffffff"

    slides:
      - type: title
        title: "Main Title"
        subtitle: "Subtitle text"

      - type: section
        title: "Section Header"

      - type: content
        title: "Slide Title"
        body: |
          First bullet point
          Second bullet point
          Third bullet point
        notes: "Speaker notes for this slide"

      - type: two_column
        title: "Slide Title"
        left: |
          Left column content
          Second line
        right: |
          Right column content
          Second line
        notes: "Speaker notes"

      - type: table
        title: "Slide Title"
        headers: ["Column 1", "Column 2", "Column 3"]
        rows:
          - ["cell 1", "cell 2", "cell 3"]
          - ["cell 4", "cell 5", "cell 6"]
        notes: "Speaker notes"

      - type: quote
        title: "Slide Title"
        quote: "The quoted text"
        attribution: "— Source"
        notes: "Speaker notes"
"""

import sys
import yaml
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def hex_to_rgb(hex_str):
    """Convert hex string (no #) to RGBColor."""
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_text(tf, text, font_name, font_size, color, bold=False, alignment=PP_ALIGN.LEFT):
    """Set text on a text frame with formatting."""
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = alignment


def add_bullets(tf, lines, font_name, font_size, color):
    """Add bulleted lines to a text frame."""
    tf.clear()
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
        p.text = line
        p.font.name = font_name
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
        p.level = 0


def add_speaker_notes(slide, notes_text, font_name):
    """Add speaker notes to a slide."""
    if not notes_text:
        return
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text
    for p in tf.paragraphs:
        p.font.name = font_name
        p.font.size = Pt(11)


def make_title_slide(prs, spec, theme):
    """Create a title slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    # Background
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_bg", "ffffff"))

    # Title
    left = Inches(0.8)
    top = Inches(2.0)
    width = Inches(8.4)
    height = Inches(1.5)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    set_text(tf, spec.get("title", ""), theme["font_heading"], 36,
             hex_to_rgb(theme["color_heading"]), bold=True, alignment=PP_ALIGN.LEFT)

    # Subtitle
    if spec.get("subtitle"):
        top2 = Inches(3.6)
        height2 = Inches(1.0)
        txBox2 = slide.shapes.add_textbox(left, top2, width, height2)
        tf2 = txBox2.text_frame
        set_text(tf2, spec["subtitle"], theme["font_body"], 18,
                 hex_to_rgb(theme["color_body"]), alignment=PP_ALIGN.LEFT)

    # Accent line
    line_top = Inches(3.4)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, line_top, Inches(2.0), Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(theme["color_accent"])
    shape.line.fill.background()

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


def make_section_slide(prs, spec, theme):
    """Create a section divider slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_heading", "1a1a2e"))

    left = Inches(0.8)
    top = Inches(2.5)
    width = Inches(8.4)
    height = Inches(2.0)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    set_text(tf, spec.get("title", ""), theme["font_heading"], 32,
             RGBColor(0xFF, 0xFF, 0xFF), bold=True, alignment=PP_ALIGN.LEFT)

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


def make_content_slide(prs, spec, theme):
    """Create a standard bullet-point slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_bg", "ffffff"))

    # Title
    left = Inches(0.8)
    top = Inches(0.5)
    width = Inches(8.4)
    height = Inches(0.8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    set_text(tf, spec.get("title", ""), theme["font_heading"], 28,
             hex_to_rgb(theme["color_heading"]), bold=True)

    # Accent line under title
    line_top = Inches(1.25)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, line_top, Inches(1.5), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(theme["color_accent"])
    shape.line.fill.background()

    # Body
    body_text = spec.get("body", "")
    lines = [l for l in body_text.strip().split("\n") if l.strip()]
    body_top = Inches(1.6)
    body_height = Inches(5.0)
    txBox2 = slide.shapes.add_textbox(left, body_top, width, body_height)
    tf2 = txBox2.text_frame
    add_bullets(tf2, lines, theme["font_body"], 18, hex_to_rgb(theme["color_body"]))

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


def make_two_column_slide(prs, spec, theme):
    """Create a two-column slide."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_bg", "ffffff"))

    # Title
    left = Inches(0.8)
    top = Inches(0.5)
    width = Inches(8.4)
    height = Inches(0.8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    set_text(tf, spec.get("title", ""), theme["font_heading"], 28,
             hex_to_rgb(theme["color_heading"]), bold=True)

    # Accent line
    line_top = Inches(1.25)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, line_top, Inches(1.5), Pt(2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(theme["color_accent"])
    shape.line.fill.background()

    # Left column
    left_lines = [l for l in spec.get("left", "").strip().split("\n") if l.strip()]
    txBox_l = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(4.0), Inches(5.0))
    tf_l = txBox_l.text_frame
    add_bullets(tf_l, left_lines, theme["font_body"], 16, hex_to_rgb(theme["color_body"]))

    # Right column
    right_lines = [l for l in spec.get("right", "").strip().split("\n") if l.strip()]
    txBox_r = slide.shapes.add_textbox(Inches(5.2), Inches(1.6), Inches(4.0), Inches(5.0))
    tf_r = txBox_r.text_frame
    add_bullets(tf_r, right_lines, theme["font_body"], 16, hex_to_rgb(theme["color_body"]))

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


def make_table_slide(prs, spec, theme):
    """Create a slide with a table."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_bg", "ffffff"))

    # Title
    left = Inches(0.8)
    top = Inches(0.5)
    width = Inches(8.4)
    height = Inches(0.8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    set_text(tf, spec.get("title", ""), theme["font_heading"], 28,
             hex_to_rgb(theme["color_heading"]), bold=True)

    headers = spec.get("headers", [])
    rows = spec.get("rows", [])
    n_rows = len(rows) + 1
    n_cols = len(headers)

    table_shape = slide.shapes.add_table(
        n_rows, n_cols,
        Inches(0.8), Inches(1.6), Inches(8.4), Inches(0.5 + 0.4 * n_rows)
    )
    table = table_shape.table

    # Header row
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        for p in cell.text_frame.paragraphs:
            p.font.name = theme["font_heading"]
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.fill.solid()
        cell.fill.fore_color.rgb = hex_to_rgb(theme["color_heading"])

    # Data rows
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.name = theme["font_body"]
                p.font.size = Pt(13)
                p.font.color.rgb = hex_to_rgb(theme["color_body"])

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


def make_quote_slide(prs, spec, theme):
    """Create a slide with a centered quote."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = hex_to_rgb(theme.get("color_bg", "ffffff"))

    # Title (optional)
    if spec.get("title"):
        txBox_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8))
        tf_t = txBox_t.text_frame
        set_text(tf_t, spec["title"], theme["font_heading"], 28,
                 hex_to_rgb(theme["color_heading"]), bold=True)

    # Quote
    quote_top = Inches(2.2) if spec.get("title") else Inches(2.0)
    txBox_q = slide.shapes.add_textbox(Inches(1.5), quote_top, Inches(7.0), Inches(2.5))
    tf_q = txBox_q.text_frame
    tf_q.word_wrap = True
    p = tf_q.paragraphs[0]
    p.text = spec.get("quote", "")
    p.font.name = theme["font_body"]
    p.font.size = Pt(22)
    p.font.italic = True
    p.font.color.rgb = hex_to_rgb(theme["color_heading"])
    p.alignment = PP_ALIGN.CENTER

    # Attribution
    if spec.get("attribution"):
        txBox_a = slide.shapes.add_textbox(Inches(1.5), Inches(4.8), Inches(7.0), Inches(0.5))
        tf_a = txBox_a.text_frame
        set_text(tf_a, spec["attribution"], theme["font_body"], 14,
                 hex_to_rgb(theme["color_accent"]), alignment=PP_ALIGN.CENTER)

    add_speaker_notes(slide, spec.get("notes", ""), theme["font_body"])
    return slide


SLIDE_BUILDERS = {
    "title": make_title_slide,
    "section": make_section_slide,
    "content": make_content_slide,
    "two_column": make_two_column_slide,
    "table": make_table_slide,
    "quote": make_quote_slide,
}


def generate(input_path, output_path):
    """Generate a .pptx from a YAML slide spec."""
    with open(input_path, "r") as f:
        spec = yaml.safe_load(f)

    theme = spec.get("theme", {})
    theme.setdefault("font_heading", "Helvetica")
    theme.setdefault("font_body", "Helvetica")
    theme.setdefault("color_heading", "1a1a2e")
    theme.setdefault("color_accent", "c0392b")
    theme.setdefault("color_body", "2c3e50")
    theme.setdefault("color_bg", "ffffff")

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    for slide_spec in spec.get("slides", []):
        slide_type = slide_spec.get("type", "content")
        builder = SLIDE_BUILDERS.get(slide_type, make_content_slide)
        builder(prs, slide_spec, theme)

    prs.save(output_path)
    print(f"Generated: {output_path} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generate_pptx.py <input.yaml> <output.pptx>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
