#!/usr/bin/env python3
"""
Generate JLPT N5 Mock Test dataset with rich HTML Furigana readings above Kanji
"""

import json
import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

questions_n5 = [
    # もんだい 1
    {
        "id": "q1",
        "num": 1,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "① あの <ruby><span class=\"highlight-target\">先生</span><rt>せんせい</rt></ruby>は わかいです。",
        "options": ["1 せんせえ", "2 せんせい", "3 せんせん", "4 せんせ"],
        "answer": 1, # choice 2 -> 0-indexed: 1
        "explanation": "先生 (せんせい) means teacher."
    },
    {
        "id": "q2",
        "num": 2,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "② あした えいがかんは <ruby><span class=\"highlight-target\">休み</span><rt>やすみ</rt></ruby>です。",
        "options": ["1 やつみ", "2 やづみ", "3 やすみ", "4 やずみ"],
        "answer": 2, # choice 3
        "explanation": "休み (やすみ) means holiday / closed."
    },
    {
        "id": "q3",
        "num": 3,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "③ この セーターは <ruby><span class=\"highlight-target\">二千九百</span><rt>にせんきゅうひゃく</rt></ruby>えんでした。",
        "options": ["1 にっせんきゅうひゃく", "2 にっせんくひゃく", "3 にせんきゅうびゃく", "4 にせんきゅうひゃく"],
        "answer": 3, # choice 4
        "explanation": "二千九百 (にせんきゅうひゃく) = 2,900 yen."
    },
    {
        "id": "q4",
        "num": 4,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "④ すみません、<ruby><span class=\"highlight-target\">お金</span><rt>おかね</rt></ruby>を わすれました。",
        "options": ["1 おかね", "2 おかぬ", "3 おがね", "4 おがぬ"],
        "answer": 0, # choice 1
        "explanation": "お金 (おかね) means money."
    },
    {
        "id": "q5",
        "num": 5,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑤ まいにち <ruby><span class=\"highlight-target\">大学</span><rt>だいがく</rt></ruby>へ いきます。",
        "options": ["1 たいがく", "2 だいがく", "3 たいかく", "4 だいかく"],
        "answer": 1, # choice 2
        "explanation": "大学 (だいがく) means university."
    },
    {
        "id": "q6",
        "num": 6,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑥ わたしは <ruby><span class=\"highlight-target\">雨</span><rt>あめ</rt></ruby>の 日が すきです。",
        "options": ["1 あめ", "2 ゆき", "3 かぜ", "4 くも"],
        "answer": 0, # choice 1
        "explanation": "雨 (あめ) means rain."
    },
    {
        "id": "q7",
        "num": 7,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑦ この <ruby><span class=\"highlight-target\">魚</span><rt>さかな</rt></ruby>は あたらしいです。",
        "options": ["1 にく", "2 たまご", "3 やさい", "4 さかな"],
        "answer": 3, # choice 4
        "explanation": "魚 (さかな) means fish."
    },
    {
        "id": "q8",
        "num": 8,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑧ あさって <ruby><span class=\"highlight-target\">友だち</span><rt>ともだち</rt></ruby>が きます。",
        "options": ["1 ともだち", "2 きょうだい", "3 かぞく", "4 りょうしん"],
        "answer": 0, # choice 1
        "explanation": "友だち (ともだち) means friend."
    },
    {
        "id": "q9",
        "num": 9,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑨ <ruby><span class=\"highlight-target\">北</span><rt>きた</rt></ruby>の ほうへ あるきましょう。",
        "options": ["1 みなみ", "2 にし", "3 きた", "4 ひがし"],
        "answer": 2, # choice 3
        "explanation": "北 (きた) means north."
    },
    {
        "id": "q10",
        "num": 10,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 1",
        "rubyHtml": "⑩ 毎朝 <ruby><span class=\"highlight-target\">新聞</span><rt>しんぶん</rt></ruby>を よみます。",
        "options": ["1 ざっし", "2 しんぶん", "3 ほん", "4 てがみ"],
        "answer": 1, # choice 2
        "explanation": "新聞 (しんぶん) means newspaper."
    },

    # もんだい 2 (Hiragana -> Kanji)
    {
        "id": "q11",
        "num": 11,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 2",
        "rubyHtml": "⑪ テーブルの うえに <ruby><span class=\"highlight-target\">ほん</span><rt></rt></ruby>が あります。",
        "options": ["1 本", "2 木", "3 林", "4 森"],
        "answer": 0, # choice 1
        "explanation": "ほん is written as 本."
    },
    {
        "id": "q12",
        "num": 12,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 2",
        "rubyHtml": "⑫ わたしの <ruby><span class=\"highlight-target\">ちち</span><rt></rt></ruby>は 50さいです。",
        "options": ["1 母", "2 兄", "3 弟", "4 父"],
        "answer": 3, # choice 4
        "explanation": "ちち (my father) is written as 父."
    },
    {
        "id": "q13",
        "num": 13,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 2",
        "rubyHtml": "⑬ くるまで <ruby><span class=\"highlight-target\">いっしょに</span><rt></rt></ruby> いきます。",
        "options": ["1 一書に", "2 一緒に", "3 一生に", "4 一所に"],
        "answer": 1, # choice 2
        "explanation": "いっしょに (together) is written as 一緒に."
    },
    {
        "id": "q14",
        "num": 14,
        "sectionId": "vocab",
        "sectionTitle": "言語知識（文字・語彙）- もんだい 2",
        "rubyHtml": "⑭ <ruby><span class=\"highlight-target\">みず</span><rt></rt></ruby>を のみます。",
        "options": ["1 火", "2 木", "3 水", "4 土"],
        "answer": 2, # choice 3
        "explanation": "みず (water) is written as 水."
    },

    # 文法 (Grammar)
    {
        "id": "q15",
        "num": 15,
        "sectionId": "grammar",
        "sectionTitle": "言語知識（文法）- もんだい 1",
        "rubyHtml": "⑮ わたしは <ruby>毎朝<rt>まいあさ</rt></ruby> 7時<ruby><span class=\"highlight-target\">__</span><rt></rt></ruby> おきます。",
        "options": ["1 に", "2 で", "3 を", "4 へ"],
        "answer": 0, # choice 1
        "explanation": "Time particle に indicates specific time (7時に)."
    },
    {
        "id": "q16",
        "num": 16,
        "sectionId": "grammar",
        "sectionTitle": "言語知識（文法）- もんだい 1",
        "rubyHtml": "⑯ 図書館<ruby><span class=\"highlight-target\">__</span><rt></rt></ruby> <ruby>日本語<rt>にほんご</rt></ruby>を <ruby>勉強<rt>べんきょう</rt></ruby>します。",
        "options": ["1 に", "2 で", "3 を", "4 から"],
        "answer": 1, # choice 2
        "explanation": "Action location particle で indicates location of activity (図書館で)."
    },

    # 読解 (Reading)
    {
        "id": "q17",
        "num": 17,
        "sectionId": "reading",
        "sectionTitle": "読解（Reading Comprehension）",
        "passageHtml": "【<ruby>読解<rt>どっかい</rt></ruby>】\nわたしは リーです。まいあさ 7じに おきます。あさごはんを たべてから、バスで がっこうへ いきます。がっこうは 9じから 3じまで です。きょうの ごごは としょかんで にほんごの べんきょうを しました。",
        "rubyHtml": "十七. リーさんは きょうの ごご なにを しましたか。",
        "options": [
            "1 としょかんで にほんごの べんきょうを しました。",
            "2 バスで がっこうへ いきました。",
            "3 7じに おきました。",
            "4 あさごはんを たべました。"
        ],
        "answer": 0, # choice 1
        "explanation": "Passage states: 'きょうの ごごは としょかんで にほんごの べんきょうを しました。'"
    }
]

quiz_data = {
    "id": "jlpt-n5-mock-exam-set",
    "title": "JLPT N5 Mock Exam Set",
    "level": "N5",
    "timeLimitMinutes": 45,
    "passingScore": 80,
    "maxScore": 180,
    "sections": [
        {
            "id": "vocab",
            "title": "言語知識（文字・語彙）",
            "weight": 60,
            "questions": [q for q in questions_n5 if q["sectionId"] == "vocab"]
        },
        {
            "id": "grammar",
            "title": "言語知識（文法）",
            "weight": 60,
            "questions": [q for q in questions_n5 if q["sectionId"] == "grammar"]
        },
        {
            "id": "reading",
            "title": "読解（Reading Comprehension）",
            "weight": 60,
            "questions": [q for q in questions_n5 if q["sectionId"] == "reading"]
        }
    ]
}

out_json = r'c:\Users\Administrator\Pictures\mock test\data\n5_practice_set_9.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print("✅ Generated JLPT N5 Furigana HTML dataset at data/n5_practice_set_9.json!")
