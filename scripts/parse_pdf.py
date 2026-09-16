#!/usr/bin/env python3
"""
JLPT PDF Question Parser Tool
Extracts questions, multiple choice options (1,2,3,4 / A,B,C,D), and answers from test PDFs.

Usage:
  python scripts/parse_pdf.py --pdf my_test.pdf --output data/my_test.json --level N5 --title "JLPT N5 Practice Test 2"
"""

import sys
import os
import json
import re
import argparse

def parse_text_to_quiz_json(text_content, level="N5", title="Custom JLPT Mock Test"):
    """
    Parses raw text extracted from PDF into a structured JLPT Mock Test JSON.
    Recognizes question patterns like:
    問題1 ...
    1. きょうは **日曜日** です。
      (1) にちようび
      (2) げつようび
      (3) すいようび
      (4) きんようび
    """

    sections = [
      {
        "id": "vocab",
        "title": "Language Knowledge (Vocabulary)",
        "weight": 60,
        "questions": []
      },
      {
        "id": "grammar",
        "title": "Language Knowledge (Grammar)",
        "weight": 60,
        "questions": []
      },
      {
        "id": "reading",
        "title": "Reading Comprehension",
        "weight": 60,
        "questions": []
      }
      # Listening (聴解) questions automatically skipped per user policy
    ]

    # Simple regex parsing heuristic for questions & options
    lines = text_content.split('\n')
    current_q = None
    q_counter = 1

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue

        # Question header match e.g. "1. ..." or "Q1. ..." or "問1 ..."
        q_match = re.match(r'^(?:問題|問|Q|\d+[\.\)])\s*(.+)', line_str, re.IGNORECASE)
        opt_match = re.match(r'^(?:[\(（]?([1-4A-Da-d])[\)）\.\s]+)(.+)', line_str)

        if q_match and not opt_match:
            if current_q and len(current_q.get("options", [])) >= 2:
                sections[0]["questions"].append(current_q)

            q_text = q_match.group(1)
            current_q = {
                "id": f"q{q_counter}",
                "text": q_text,
                "options": [],
                "answer": 0,  # Default first option as answer until mapped
                "explanation": "Extracted from PDF."
            }
            q_counter += 1

        elif opt_match and current_q:
            opt_val = opt_match.group(2).strip()
            current_q["options"].append(opt_val)

    if current_q and len(current_q.get("options", [])) >= 2:
        sections[0]["questions"].append(current_q)

    # Fallback if no questions detected automatically
    if sum(len(s["questions"]) for s in sections) == 0:
        print("⚠️ Warning: Could not auto-structure regex questions. Creating template JSON from PDF text...")
        sections[0]["questions"].append({
            "id": "q1",
            "text": "Sample Question extracted from PDF text",
            "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "answer": 0,
            "explanation": text_content[:200] + "..."
        })

    return {
        "id": f"jlpt-{level.lower()}-extracted",
        "title": title,
        "level": level.upper(),
        "timeLimitMinutes": 45 if level.upper() in ["N5", "N4"] else 70,
        "passingScore": 80 if level.upper() in ["N5", "N4"] else 95,
        "maxScore": 180,
        "sections": sections
    }

def main():
    parser = argparse.ArgumentParser(description="JLPT PDF Question Converter")
    parser.add_argument("--pdf", type=str, help="Path to input PDF file")
    parser.add_argument("--output", type=str, default="data/custom_test.json", help="Path to output JSON")
    parser.add_argument("--level", type=str, default="N5", help="JLPT Level (N5, N4, N3, N2, N1)")
    parser.add_argument("--title", type=str, default="JLPT Mock Exam", help="Title of test")
    args = parser.parse_args()

    if not args.pdf or not os.path.exists(args.pdf):
        print("Usage: python scripts/parse_pdf.py --pdf <your_pdf_file.pdf> --output <output.json>")
        print("\nNote: You can also manually copy/paste questions into data/sample_n5.json format.")
        sys.exit(1)

    print(f"📄 Reading PDF file: {args.pdf}...")

    # Try pypdf or PyPDF2 if installed
    extracted_text = ""
    try:
        import pypdf
        reader = pypdf.PdfReader(args.pdf)
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
    except ImportError:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(args.pdf)
            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"
        except ImportError:
            print("❌ PyPDF library not found. Install with: pip install pypdf")
            sys.exit(1)

    quiz_data = parse_text_to_quiz_json(extracted_text, level=args.level, title=args.title)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Extracted test JSON saved successfully to: {args.output}")

if __name__ == '__main__':
    main()
