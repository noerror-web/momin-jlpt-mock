#!/usr/bin/env python3
"""
Smart OCR Question Cropper
Extracts exact single-question snippet cards for JLPT Mock Test
"""

import pymupdf
import io
import os
import sys
import re
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

pdf_path = r'C:\Users\Administrator\Downloads\AyuGram Desktop\N5 PRACTICE SET (9).pdf'
out_dir = r'c:\Users\Administrator\Pictures\mock test\public\n5_questions'
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
ocr = RapidOCR()

def smart_crop_pdf():
    q_global_index = 1
    
    # Process pages 2 to 67
    for page_num in range(1, len(doc) - 2):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes('png')
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size

        res, _ = ocr(img_bytes)
        if not res:
            continue

        # Find line blocks starting with question indicators (e.g. ①, ②, 1., 2., 問1, もんだい)
        question_starts = []
        for line in res:
            box, text, score = line
            text_str = text.strip()
            # Check if this line is a question start
            is_q_start = False
            if re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩]', text_str):
                is_q_start = True
            elif re.match(r'^(?:問|問題|\d+[\.\)])', text_str):
                is_q_start = True

            if is_q_start:
                y_min = min(pt[1] for pt in box)
                question_starts.append((y_min, text_str))

        if not question_starts:
            # Fallback for pages without clear number headers
            continue

        question_starts.sort(key=lambda x: x[0])

        # Crop between question starts
        for idx in range(len(question_starts)):
            y_start = max(0, int(question_starts[idx][0]) - 25)
            if idx + 1 < len(question_starts):
                y_end = int(question_starts[idx + 1][0]) - 15
            else:
                y_end = min(h, int(question_starts[idx][0]) + 300)

            if y_end - y_start < 50:
                continue

            crop_box = (30, y_start, w - 30, y_end)
            cropped_img = img.crop(crop_box)

            q_path = os.path.join(out_dir, f"q_{q_global_index}.png")
            cropped_img.save(q_path)
            q_global_index += 1

    print(f"✅ Created {q_global_index - 1} exact question card snippets!")

if __name__ == '__main__':
    smart_crop_pdf()
