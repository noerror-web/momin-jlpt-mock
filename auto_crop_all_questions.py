#!/usr/bin/env python3
"""
Crop individual clean question items from N5 PRACTICE SET (9).pdf
Generates single-question card images: q1.png, q2.png, q3.png...
"""

import pymupdf
import io
import os
import sys
from PIL import Image

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

pdf_path = r'C:\Users\Administrator\Downloads\AyuGram Desktop\N5 PRACTICE SET (9).pdf'
out_dir = r'c:\Users\Administrator\Pictures\mock test\public\n5_questions'
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)

# Page mapping for N5 Vocabulary (Pages 2 to 19)
# We crop each question into a neat box (approx 120-180px height depending on page layout)

def extract_cropped_questions():
    q_counter = 1

    # Pages 2 to 19 (Vocabulary: もんだい 1 to もんだい 4)
    for p_idx in range(1, 20):
        page = doc[p_idx]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes('png')))
        w, h = img.size

        # Exclude page header & footer margins (top 12%, bottom 8%)
        top_margin = int(h * 0.12)
        bottom_margin = int(h * 0.92)
        content_h = bottom_margin - top_margin

        # Crop 4-5 items per page
        items_per_page = 4
        item_h = content_h // items_per_page

        for i in range(items_per_page):
            y1 = top_margin + (i * item_h)
            y2 = min(y1 + item_h + 20, h - 20)

            # Crop item
            q_crop = img.crop((40, y1, w - 40, y2))
            
            # Save snippet image
            q_path = os.path.join(out_dir, f"q_{q_counter}.png")
            q_crop.save(q_path)

            q_counter += 1

    print(f"✅ Generated {q_counter - 1} cropped question snippets!")

if __name__ == '__main__':
    extract_cropped_questions()
