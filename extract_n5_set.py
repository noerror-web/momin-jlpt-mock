#!/usr/bin/env python3
"""
Extract N5 Practice Set (9).pdf into web page images and generate full test dataset JSON
"""

import pymupdf
import json
import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

pdf_path = r'C:\Users\Administrator\Downloads\AyuGram Desktop\N5 PRACTICE SET (9).pdf'
out_img_dir = r'c:\Users\Administrator\Pictures\mock test\public\n5_pages'
os.makedirs(out_img_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
print(f"Exporting {len(doc)} PDF pages to images...")

for i in range(len(doc)):
    page_img_path = os.path.join(out_img_dir, f"page_{i+1}.png")
    if not os.path.exists(page_img_path):
        pix = doc[i].get_pixmap(dpi=150)
        pix.save(page_img_path)

print("✅ Page images exported!")

# Answer key from Page 69
# Section 1: Vocabulary (文字・語彙)
# もんだい 1: 1:2, 2:3, 3:4, 4:1, 5:2, 6:1, 7:4, 8:1, 9:3, 10:2, 11:3, 12:4, 13:2, 14:3, 15:1, 16:2, 17:1, 18:3 (1-based choice: 0-indexed is choice - 1)
# もんだい 2: 19:4, 20:3, 21:2, 22:4, 23:1, 24:1, 25:3, 26:4, 27:1, 28:2, 29:2, 30:4
# もんだい 3: 31:2, 32:4, 33:3, 34:4, 35:2, 36:1, 37:2, 38:1, 39:3, 40:1, 41:4, 42:3, 43:3, 44:1, 45:1
# もんだい 4: 46:4, 47:3, 48:1, 49:4, 50:2, 51:1, 52:3

vocab_answers = {
    1: 2, 2: 3, 3: 4, 4: 1, 5: 2, 6: 1, 7: 4, 8: 1, 9: 3, 10: 2, 11: 3, 12: 4, 13: 2, 14: 3, 15: 1, 16: 2, 17: 1, 18: 3,
    19: 4, 20: 3, 21: 2, 22: 4, 23: 1, 24: 1, 25: 3, 26: 4, 27: 1, 28: 2, 29: 2, 30: 4,
    31: 2, 32: 4, 33: 3, 34: 4, 35: 2, 36: 1, 37: 2, 38: 1, 39: 3, 40: 1, 41: 4, 42: 3, 43: 3, 44: 1, 45: 1,
    46: 4, 47: 3, 48: 1, 49: 4, 50: 2, 51: 1, 52: 3
}

# Section 2: Grammar (文法)
# もんだい 1: 1:2, 2:4, 3:3, 4:2, 5:1, 6:2, 7:3, 8:4, 9:3, 10:4, 11:1, 12:2, 13:3, 14:2, 15:4, 16:1, 17:3, 18:4, 19:3, 20:1, 21:3, 22:2, 23:3, 24:4
# もんだい 2: 25:2, 26:3, 27:2, 28:1, 29:4, 30:4, 31:2
# もんだい 3: 32:3, 33:1, 34:4, 35:3, 36:4

grammar_answers = {
    1: 2, 2: 4, 3: 3, 4: 2, 5: 1, 6: 2, 7: 3, 8: 4, 9: 3, 10: 4, 11: 1, 12: 2, 13: 3, 14: 2, 15: 4, 16: 1, 17: 3, 18: 4, 19: 3, 20: 1, 21: 3, 22: 2, 23: 3, 24: 4,
    25: 2, 26: 3, 27: 2, 28: 1, 29: 4, 30: 4, 31: 2,
    32: 3, 33: 1, 34: 4, 35: 3, 36: 4
}

# Section 3: Reading (読解)
# もんだい 1: 1:4
# もんだい 2: 2:3
# もんだい 3: 3:2
# もんだい 4: 4:2

reading_answers = {
    1: 4, 2: 3, 3: 2, 4: 2
}

def build_questions(sec_title, ans_dict, start_idx, total_q):
    questions = []
    for q_num in range(1, total_q + 1):
        correct_opt = ans_dict[q_num] - 1 # 1-4 to 0-3
        snippet_idx = start_idx + (q_num - 1)
        questions.append({
            "id": f"q_{sec_title.lower()}_{q_num}",
            "num": q_num,
            "text": f"Question {q_num}",
            "questionCardImage": f"public/n5_questions/q_{min(snippet_idx, 76)}.png",
            "options": ["1", "2", "3", "4"],
            "answer": correct_opt,
            "explanation": f"Official Tanki Master Answer: Choice ({ans_dict[q_num]})"
        })
    return questions

quiz_data = {
    "id": "jlpt-n5-practice-set-9",
    "title": "JLPT N5 Official Tanki Master Practice Exam",
    "level": "N5",
    "timeLimitMinutes": 50,
    "passingScore": 80,
    "maxScore": 180,
    "sections": [
        {
            "id": "vocab",
            "title": "言語知識 (文字・語彙)",
            "weight": 60,
            "questions": build_questions("vocab", vocab_answers, 1, 52)
        },
        {
            "id": "grammar",
            "title": "言語知識 (文法)",
            "weight": 60,
            "questions": build_questions("grammar", grammar_answers, 53, 36)
        },
        {
            "id": "reading",
            "title": "読解 (Reading Comprehension)",
            "weight": 60,
            "questions": build_questions("reading", reading_answers, 70, 4)
        }
    ]
}

out_json = r'c:\Users\Administrator\Pictures\mock test\data\n5_practice_set_9.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print(f"✅ Generated full N5 practice test dataset at: {out_json}")
