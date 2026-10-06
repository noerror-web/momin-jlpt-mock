#!/usr/bin/env python3
"""
Generate JLPT N5 Mock Test Set 2 Dataset (83 Questions from PDF)
"""

import json
import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Answer key mapping from PDF page 10 (1-indexed choice index: A=1, B=2, C=3, D=4)
# Converted to 0-indexed for json (A=0, B=1, C=2, D=3)
raw_answer_key = {
    # Section 1: Vocab (1-25)
    1: 4, 2: 3, 3: 4, 4: 3, 5: 4, 6: 4, 7: 3, 8: 3, 9: 1, 10: 3,
    11: 4, 12: 4, 13: 3, 14: 4, 15: 1, 16: 2, 17: 4, 18: 3, 19: 4, 20: 1,
    21: 1, 22: 1, 23: 4, 24: 3, 25: 2,

    # Section 2: Particles & Grammar (26-65)
    26: 3, 27: 4, 28: 3, 29: 3, 30: 1, 31: 2, 32: 1, 33: 1, 34: 3, 35: 3,
    36: 4, 37: 2, 38: 1, 39: 1, 40: 4, 41: 3, 42: 3, 43: 4, 44: 2, 45: 2,
    46: 2, 47: 4, 48: 3, 49: 2, 50: 4, 51: 4, 52: 4, 53: 1, 54: 1, 55: 2,
    56: 1, 57: 1, 58: 4, 59: 4, 60: 2,
    61: 3, 62: 2, 63: 3, 64: 2, 65: 3,

    # Section 3: Reading (66-83)
    66: 4, 67: 3, 68: 3, 69: 1, 70: 2, 71: 3, 72: 3, 73: 4, 74: 1, 75: 2,
    76: 4, 77: 3, 78: 3, 79: 2, 80: 2, 81: 4, 82: 4, 83: 4
}

vocab_questions_data = [
    # Part 1 — Kanji Reading (1-10)
    ("① きのう「<span class=\"highlight-target\">友達</span>」と あそびました。", ["A) ゆうだち", "B) ゆうたつ", "C) ともたち", "D) ともだち"], "友達 (ともだち) means 'friend'."),
    ("② 「<span class=\"highlight-target\">先生</span>」に しつもんします。", ["A) さきしょう", "B) せんしょう", "C) せんせい", "D) さきせい"], "先生 (せんせい) means 'teacher'."),
    ("③ 「<span class=\"highlight-target\">時間</span>」が ありません。", ["A) ときま", "B) ときかん", "C) じま", "D) じかん"], "時間 (じかん) means 'time'."),
    ("④ この「<span class=\"highlight-target\">道</span>」を まっすぐ いってください。", ["A) どう", "B) つう", "C) みち", "D) とお"], "道 (みち) means 'street' / 'road'."),
    ("⑤ 「<span class=\"highlight-target\">母</span>」は りょうりが じょうずです。", ["A) ぼ", "B) あね", "C) おば", "D) はは"], "母 (はは) means 'my mother'."),
    ("⑥ 「<span class=\"highlight-target\">会社</span>」に つとめています。", ["A) あいしゃ", "B) えしゃ", "C) かいじゃ", "D) かいしゃ"], "会社 (かいしゃ) means 'company' / 'office'."),
    ("⑦ 「<span class=\"highlight-target\">手紙</span>」を かきました。", ["A) てし", "B) しゅし", "C) てがみ", "D) しゅがみ"], "手紙 (てがみ) means 'letter'."),
    ("⑧ 「<span class=\"highlight-target\">来週</span>」テストが あります。", ["A) きしゅう", "B) くしゅう", "C) らいしゅう", "D) らいしゅ"], "来週 (らいしゅう) means 'next week'."),
    ("⑨ 「<span class=\"highlight-target\">名前</span>」を ここに かいてください。", ["A) なまえ", "B) なぜん", "C) めいまえ", "D) めいぜん"], "名前 (なまえ) means 'name'."),
    ("⑩ 「<span class=\"highlight-target\">今朝</span>」パンを たべました。", ["A) こんちょう", "B) きんあさ", "C) けさ", "D) いまあさ"], "今朝 (けさ) means 'this morning'."),

    # Part 2 — Kanji Writing (11-20)
    ("⑪ 「<span class=\"highlight-target\">かわ</span>」の ちかくに すんでいます。", ["A) 池", "B) 山", "C) 海", "D) 川"], "かわ (river) is written in Kanji as 川."),
    ("⑫ 「<span class=\"highlight-target\">しろ</span>」い くつを かいました。", ["A) 目", "B) 自", "C) 百", "D) 白"], "しろい (white) is written in Kanji as 白い."),
    ("⑬ 「<span class=\"highlight-target\">あたら</span>」しい かばんです。", ["A) 近", "B) 親", "C) 新", "D) 薪"], "あたらしい (new) is written in Kanji as 新しい."),
    ("⑭ 「<span class=\"highlight-target\">なか</span>」に はいって ください。", ["A) 入", "B) 仲", "C) 内", "D) 中"], "なか (inside) is written in Kanji as 中."),
    ("⑮ 「<span class=\"highlight-target\">そと</span>」で あそびましょう。", ["A) 外", "B) 出", "C) 大", "D) 門"], "そと (outside) is written in Kanji as 外."),
    ("⑯ 「<span class=\"highlight-target\">ひだり</span>」に まがります。", ["A) 下", "B) 左", "C) 上", "D) 右"], "ひだり (left) is written in Kanji as 左."),
    ("⑰ 「<span class=\"highlight-target\">おんな</span>」の こが います。", ["A) 男", "B) 母", "C) 子", "D) 女"], "おんな (female/woman) is written in Kanji as 女."),
    ("⑱ 「<span class=\"highlight-target\">ゆき</span>」が ふりました。", ["A) 雨", "B) 雷", "C) 雪", "D) 雲"], "ゆき (snow) is written in Kanji as 雪."),
    ("⑲ 「<span class=\"highlight-target\">にし</span>」に いきます。", ["A) 北", "B) 南", "C) 東", "D) 西"], "にし (west) is written in Kanji as 西."),
    ("⑳ 「<span class=\"highlight-target\">いもうと</span>」は こうこうせいです。", ["A) 妹", "B) 姉", "C) 弟", "D) 兄"], "いもうと (younger sister) is written in Kanji as 妹."),

    # Part 3 — Vocabulary in Context (21-25)
    ("㉑ テーブルの うえに コップが みっつ<span class=\"highlight-target\">（　）</span>。", ["A) あります", "B) します", "C) なります", "D) います"], "Inanimate objects like cups (コップ) use あります."),
    ("㉒ えきで でんしゃを<span class=\"highlight-target\">（　）</span>。", ["A) まちます", "B) おしえます", "C) つくります", "D) あるきます"], "まちます means 'wait' (waiting for train at station)."),
    ("㉓ しけんは<span class=\"highlight-target\">（　）</span>でしたか。", ["A) どれ", "B) どんな", "C) どの", "D) どう"], "どうでしたか asks 'How was [the exam]?''."),
    ("㉔ あの みせの ラーメンは とても<span class=\"highlight-target\">（　）</span>です。", ["A) ちかい", "B) ほそい", "C) おいしい", "D) ひろい"], "おいしい (delicious) fits ramen best."),
    ("㉕ まどを<span class=\"highlight-target\">（　）</span>ください。あついですから。", ["A) けして", "B) あけて", "C) しめて", "D) つけて"], "あけて (open) the window because it is hot.")
]

grammar_questions_data = [
    # Part 4 — Particles (26-45)
    ("㉖ まいあさ ぎゅうにゅう<span class=\"highlight-target\">（　）</span>のみます。", ["A) が", "B) で", "C) を", "D) に"], "Direct object marker を with verb のみます."),
    ("㉗ きょうしつ<span class=\"highlight-target\">（　）</span>にほんごを べ勉強します。", ["A) に", "B) が", "C) を", "D) で"], "Action location particle で indicates location of activity."),
    ("㉘ にちようび<span class=\"highlight-target\">（　）</span>えいがを みました。", ["A) を", "B) が", "C) に", "D) で"], "Specific day/time marker に (にちようびに)."),
    ("㉙ おとうと<span class=\"highlight-target\">（　）</span>サッカーが すきです。", ["A) に", "B) を", "C) は", "D) で"], "Topic marker は (おとうとは)."),
    ("㉚ どこ<span class=\"highlight-target\">（　）</span>いきますか。", ["A) に", "B) を", "C) は", "D) が"], "Direction/Destination particle に (どこに)."),
    ("㉛ ペン<span class=\"highlight-target\">（　）</span>かして ください。", ["A) が", "B) を", "C) に", "D) で"], "Direct object particle を (ペンを)."),
    ("㉜ きょねん にほん<span class=\"highlight-target\">（　）</span>いきました。", ["A) に", "B) が", "C) を", "D) で"], "Destination particle に (にほんに)."),
    ("㉝ この へや<span class=\"highlight-target\">（　）</span>きれいですね。", ["A) は", "B) を", "C) に", "D) で"], "Topic marker は (このへやは)."),
    ("㉞ あね<span class=\"highlight-target\">（　）</span>けっこんしました。", ["A) を", "B) で", "C) が", "D) に"], "Subject marker が with intransitive state change (あねが けっこんしました)."),
    ("㉟ ちち<span class=\"highlight-target\">（　）</span>ははは きょうし です。", ["A) が", "B) は", "C) と", "D) を"], "Connecting particle と ('father AND mother')."),
    ("㊱ えき<span class=\"highlight-target\">（　）</span>バスに のります。", ["A) を", "B) に", "C) が", "D) で"], "Location of action で (えきで バスに のります)."),
    ("㊲ テスト<span class=\"highlight-target\">（　）</span>むずかしかったです。", ["A) を", "B) は", "C) に", "D) が"], "Topic marker は (テストは)."),
    ("㊳ わたしは すし<span class=\"highlight-target\">（　）</span>てんぷら<span class=\"highlight-target\">（　）</span>すきです。", ["A) も / も", "B) が / が", "C) と / と", "D) を / を"], "Dual particle も / も ('both sushi AND tempura')."),
    ("㊴ おかあさん<span class=\"highlight-target\">（　）</span>プレゼントを もらいました。", ["A) から", "B) に", "C) を", "D) で"], "Source particle から ('received from mother')."),
    ("㊵ あたらしい くつ<span class=\"highlight-target\">（　）</span>かいたいです。", ["A) で", "B) を", "C) に", "D) が"], "Target of desire -たい is marked by が (くつが かいたい)."),
    ("㊶ ここ<span class=\"highlight-target\">（　）</span>しゃしんを とりましょう。", ["A) が", "B) に", "C) で", "D) を"], "Location of action で (ここで)."),
    ("㊷ あした<span class=\"highlight-target\">（　）</span>あめが ふるでしょう。", ["A) が", "B) を", "C) は", "D) に"], "Time topic marker は (あしたは)."),
    ("㊸ テーブルの うえ<span class=\"highlight-target\">（　）</span>ほんが あります。", ["A) が", "B) で", "C) を", "D) に"], "Location of existence に (うえに)."),
    ("㊹ じてんしゃ<span class=\"highlight-target\">（　）</span>がっこうに いきます。", ["A) が", "B) で", "C) に", "D) を"], "Means/Method particle で (じてんしゃで)."),
    ("㊺ たなかさん<span class=\"highlight-target\">（　）</span>でんわを かけました。", ["A) を", "B) に", "C) が", "D) で"], "Target of call に (たなかさんに)."),

    # Part 5 — Grammar Forms (46-60)
    ("㊻ すずきさんは いま へやで ほんを<span class=\"highlight-target\">（　）</span>います。", ["A) よみ", "B) よんで", "C) よんだ", "D) よむ"], "V-て + います indicates ongoing action (よんでいます)."),
    ("㊼ しゅうまつ うみに<span class=\"highlight-target\">（　）</span>たいです。", ["A) いった", "B) いく", "C) いって", "D) いき"], "Verb stem + たい indicates desire (行きたい)."),
    ("㊽ この ケーキは<span class=\"highlight-target\">（　）</span>て おいしいです。", ["A) あまい", "B) あま", "C) あまく", "D) あまくて"], "Connecting I-adjectives: drop い and add くて (あまくて)."),
    ("㊾ きのうは がっこうに<span class=\"highlight-target\">（　）</span>。", ["A) いかなかった", "B) いきませんでした", "C) いきません", "D) いかないです"], "Past polite negative form (いきませんでした)."),
    ("㊿ たなかさんは えいごが<span class=\"highlight-target\">（　）</span>。", ["A) じょうずに", "B) じょうずな", "C) じょうずで", "D) じょうずです"], "Na-adjective polite predicate (じょうずです)."),
    ("51. まいにち いちじかん<span class=\"highlight-target\">（　）</span>うんどうします。", ["A) しか", "B) ごろ", "C) まで", "D) ぐらい"], "Approximate duration marker ぐらい ('about 1 hour')."),
    ("52. あしたは にちようびです<span class=\"highlight-target\">（　）</span>、がっこうは やすみです。", ["A) けど", "B) ので", "C) のに", "D) から"], "Conjunctive particle から indicates reason ('because tomorrow is Sunday')."),
    ("53. テレビを<span class=\"highlight-target\">（　）</span>ながら ごはんを たべます。", ["A) み", "B) みた", "C) みる", "D) みて"], "Verb stem + ながら indicates simultaneous action (みながら)."),
    ("54. この もんだいは<span class=\"highlight-target\">（　）</span>すぎます。", ["A) むずかし", "B) むずかしく", "C) むずかしくて", "D) むずかしい"], "I-adjective stem + すぎる (むずかしすぎる = too difficult)."),
    ("55. あめが ふっていますから、かさを<span class=\"highlight-target\">（　）</span>いきましょう。", ["A) もった", "B) もって", "C) もち", "D) もつ"], "V-て + いきます (もっていきましょう = let's take an umbrella and go)."),
    ("56. すみません、トイレは<span class=\"highlight-target\">（　）</span>ですか。", ["A) どこ", "B) だれ", "C) なに", "D) いつ"], "Question word どこ asks for location ('Where is the restroom?')."),
    ("57. ごはんを 食べた<span class=\"highlight-target\">（　）</span>、はを みがきます。", ["A) あとで", "B) まえに", "C) ときに", "D) あいだに"], "V-た + あとで indicates 'after doing' (食べたあとで)."),
    ("58. きょうは きのう<span class=\"highlight-target\">（　）</span>さむいです。", ["A) から", "B) まで", "C) ほど", "D) より"], "Comparison particle より ('colder than yesterday')."),
    ("59. コーヒーを いっぱい<span class=\"highlight-target\">（　）</span>しませんか。", ["A) なに", "B) どれ", "C) どう", "D) いかが"], "Offer / Suggestion phrase いかが ('How about a cup of coffee?')."),
    ("60. にほんごを<span class=\"highlight-target\">（　）</span>ことが できますか。", ["A) はなした", "B) はなす", "C) はなして", "D) はなし"], "Dictionary verb + ことが できます ('can speak Japanese')."),

    # Part 6 — Sentence Ordering (61-65)
    ("61. わたしは ＿＿ ＿＿ <span class=\"highlight-target\">★</span> ＿＿ 。", ["A) まいにち", "B) にほんご", "C) を", "D) べんきょうします"], "Correct sentence: わたしは まいにち にほんご ★を べんきょうします。(Star is C: を)."),
    ("62. きのう ＿＿ <span class=\"highlight-target\">★</span> ＿＿ ＿＿ みました。", ["A) ともだち", "B) と", "C) えいが", "D) を"], "Correct sentence: きのう ともだち ★と えいが を みました。(Star is B: と)."),
    ("63. この ＿＿ ＿＿ <span class=\"highlight-target\">★</span> ＿＿ おいしいです。", ["A) みせ", "B) の", "C) ケーキ", "D) は"], "Correct sentence: この みせ の ★ケーキ は おいしいです。(Star is C: ケーキ)."),
    ("64. ＿＿ <span class=\"highlight-target\">★</span> ＿＿ ＿＿ ならいます。", ["A) がっこうで", "B) にほんご", "C) を", "D) せんせいに"], "Correct sentence: がっこうで ★にほんご を せんせいに ならいます。(Star is B: にほんご)."),
    ("65. ＿＿ ＿＿ ＿＿ <span class=\"highlight-target\">★</span> かけます。", ["A) きのう", "B) たなかさんに", "C) でんわ", "D) を"], "Correct sentence: きのう たなかさんに でんわ ★を かけました/かけます。(Star is D/C: を).")
]

# Passages for Reading Comprehension (66-83)
reading_passages = {
    "p1": """<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【読解 1 — 自己紹介】</strong><br>
  わたしは キムです。かんこくじんです。いま とうきょうに すんでいます。<br>
  まいにち でんしゃで だいがくに いきます。だいがくで にほんごを べんきょうしています。<br>
  にほんごの じゅぎょうは ごぜん 九時から 十二時までです。<br>
  ひるごはんは いつも がくしょくで ともだちと たべます。<br>
  午後は としょかんで しゅくだいを します。<br>
  よる いえで テレビを みます。にほんの ドラマが すきです。
</div>""",

    "p2": """<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【読解 2 — パーティーのおしらせ】</strong><br>
  こんしゅうの どようびに パーティーが あります。<br>
  ばしょは すずきさんの いえです。じかんは ごご 五時からです。<br>
  わたしは ケーキを つくります。<br>
  たなかさんは のみものを かいます。<br>
  やまださんは おんがくの CDを もってきます。<br>
  みんなで うたったり おどったり します。たのしみです！
</div>""",

    "p3": """<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【読解 3 — あたらしい レストラン】</strong><br>
  わたしの まちに あたらしい レストランが できました。<br>
  イタリアりょうりの レストランです。えきから あるいて 五分です。<br>
  わたしは せんしゅうの にちようびに かぞくと いきました。<br>
  ちちは パスタを たべました。ははは サラダと ピザを たべました。<br>
  わたしは カルボナーラを たべました。とても おいしかったです。<br>
  でも すこし たかかったです。
</div>""",

    "p4": """<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【読解 4 — スケジュール】</strong><br>
  ＊＊＊ にほんご きょうしつ ＊＊＊<br>
  ・クラス： まいしゅう げつようびと すいようび<br>
  ・じかん： ごご 二時 ～ 四時<br>
  ・ばしょ： コミュニティセンター ３かい<br>
  ・せんせい： もり先生<br>
  ・もちもの： ノート、えんぴつ、きょうかしょ<br>
  ・おやすみ： しゅくじつ
</div>""",

    "p5": """<div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【読解 5 — メール】</strong><br>
  みきさんへ<br>
  こんにちは。おげんきですか。<br>
  こんどの にちようび、いっしょに こうえんで はなみを しませんか。<br>
  さくらが とても きれいですよ。<br>
  ごぜん 十時に えきの まえで あいましょう。<br>
  おべんとうは わたしが つくります。<br>
  のみものを もって きて ください。<br>
  へんじを まっています。<br>
  ゆうこ
</div>"""
}

reading_questions_data = [
    # Passage 1 (66-69)
    {
        "num": 66,
        "passageHtml": reading_passages["p1"],
        "rubyHtml": "66. キムさんは どこの 人ですか。",
        "options": ["A) にほんじん", "B) ちゅうごくじん", "C) アメリカじん", "D) かんこくじん"],
        "explanation": "Passage states: 'わたしは キムです。かんこくじんです。' (Korean)."
    },
    {
        "num": 67,
        "passageHtml": reading_passages["p1"],
        "rubyHtml": "67. だいがくまで なんで いきますか。",
        "options": ["A) じてんしゃ", "B) くるま", "C) でんしゃ", "D) バス"],
        "explanation": "Passage states: 'まいにち でんしゃで だいがくに いきます。' (Train)."
    },
    {
        "num": 68,
        "passageHtml": reading_passages["p1"],
        "rubyHtml": "68. にほんごの じゅぎょうは なんじまでですか。",
        "options": ["A) 一時", "B) 十一時", "C) 十二時", "D) 二時"],
        "explanation": "Passage states: 'ごぜん 九時から 十二時までです。' (Until 12:00)."
    },
    {
        "num": 69,
        "passageHtml": reading_passages["p1"],
        "rubyHtml": "69. 午後 キムさんは なにを しますか。",
        "options": ["A) としょかんで しゅくだい", "B) スポーツ", "C) かいもの", "D) アルアルバイト"],
        "explanation": "Passage states: '午後は としょかんで しゅくだいを します。' (Homework at library)."
    },

    # Passage 2 (70-73)
    {
        "num": 70,
        "passageHtml": reading_passages["p2"],
        "rubyHtml": "70. パーティーは なんようびですか。",
        "options": ["A) もくようび", "B) どようび", "C) きんようび", "D) にちようび"],
        "explanation": "Passage states: 'こんしゅうの どようびに パーティーが あります。' (Saturday)."
    },
    {
        "num": 71,
        "passageHtml": reading_passages["p2"],
        "rubyHtml": "71. パーティーは どこで しますか。",
        "options": ["A) こうえん", "B) レストラン", "C) すずきさんの いえ", "D) がっこう"],
        "explanation": "Passage states: 'ばしょは すずきさんの いえです。' (Suzuki's house)."
    },
    {
        "num": 72,
        "passageHtml": reading_passages["p2"],
        "rubyHtml": "72. たなかさんは なにを しますか。",
        "options": ["A) ケーキを つくる", "B) CDを もってくる", "C) のみものを かう", "D) りょうりを する"],
        "explanation": "Passage states: 'たなかさんは のみものを かいます。' (Buys drinks)."
    },
    {
        "num": 73,
        "passageHtml": reading_passages["p2"],
        "rubyHtml": "73. パーティーで なにを しますか。",
        "options": ["A) べんきょうする", "B) えいがを みる", "C) ゲームを する", "D) うたったり おどったり する"],
        "explanation": "Passage states: 'みんなで うたったり おどったり します。' (Sing and dance)."
    },

    # Passage 3 (74-77)
    {
        "num": 74,
        "passageHtml": reading_passages["p3"],
        "rubyHtml": "74. あたらしい レストランは なにりょうりの みせですか。",
        "options": ["A) イタリアりょうり", "B) ちゅうかりょうり", "C) にほんりょうり", "D) フランスりょうり"],
        "explanation": "Passage states: 'イタリアりょうりの レストランです。' (Italian food)."
    },
    {
        "num": 75,
        "passageHtml": reading_passages["p3"],
        "rubyHtml": "75. レストランは えきから どのぐらいですか。",
        "options": ["A) あるいて 十分", "B) あるいて 五分", "C) バスで 五分", "D) あるいて 三分"],
        "explanation": "Passage states: 'えきから あるいて 五分です。' (5 minutes on foot)."
    },
    {
        "num": 76,
        "passageHtml": reading_passages["p3"],
        "rubyHtml": "76. おかあさんは なにを たべましたか。",
        "options": ["A) カルボナーラ", "B) パスタ", "C) サラダだけ", "D) サラダと ピザ"],
        "explanation": "Passage states: 'ははは サラダと ピザを たべました。' (Salad and pizza)."
    },
    {
        "num": 77,
        "passageHtml": reading_passages["p3"],
        "rubyHtml": "77. レストランは どうでしたか。",
        "options": ["A) やすくて おいしい", "B) ふつうだった", "C) おいしいが たかい", "D) まずかった"],
        "explanation": "Passage states: 'とても おいしかったです。でも すこし たかかったです。' (Delicious but expensive)."
    },

    # Passage 4 (78-79)
    {
        "num": 78,
        "passageHtml": reading_passages["p4"],
        "rubyHtml": "78. にほんごの クラスは なんようびですか。",
        "options": ["A) すいようびと きんようび", "B) げつようびと きんようび", "C) げつようびと すいようび", "D) かようびと もくようび"],
        "explanation": "Notice states: 'クラス： まいしゅう げつようびと すいようび' (Mon and Wed)."
    },
    {
        "num": 79,
        "passageHtml": reading_passages["p4"],
        "rubyHtml": "79. クラスに なにを もっていきますか。",
        "options": ["A) きょうかしょだけ", "B) ノート、えんぴつ、きょうかしょ", "C) パソコンと ノート", "D) ノートと ペン"],
        "explanation": "Notice states: 'もちもの： ノート、えんぴつ、きょうかしょ'."
    },

    # Passage 5 (80-83)
    {
        "num": 80,
        "passageHtml": reading_passages["p5"],
        "rubyHtml": "80. なんようびに はなみを しますか。",
        "options": ["A) げつようび", "B) にちようび", "C) どようび", "D) きんようび"],
        "explanation": "E-mail states: 'こんどの にちようび、いっしょに こうえんで はなみを しませんか。' (Sunday)."
    },
    {
        "num": 81,
        "passageHtml": reading_passages["p5"],
        "rubyHtml": "81. どこで あいますか。",
        "options": ["A) みきさんの いえ", "B) レストラン", "C) こうえん", "D) えきの まえ"],
        "explanation": "E-mail states: 'ごぜん 十時に えきの まえで あいましょう。' (In front of station)."
    },
    {
        "num": 82,
        "passageHtml": reading_passages["p5"],
        "rubyHtml": "82. ゆうこさんは なにを つくりますか。",
        "options": ["A) ケーキ", "B) のみもの", "C) おかし", "D) おべんとう"],
        "explanation": "E-mail states: 'おべんとうは わたしが つくります。' (Bento lunchbox)."
    },
    {
        "num": 83,
        "passageHtml": reading_passages["p5"],
        "rubyHtml": "83. みきさんは なにを もっていきますか。",
        "options": ["A) おべんとう", "B) かさ", "C) カメラ", "D) のみもの"],
        "explanation": "E-mail states: 'のみものを もって きて ください。' (Drinks)."
    }
]

import re

def build_questions(sec_id, sec_title, raw_list):
    res = []
    for item in raw_list:
        if isinstance(item, tuple):
            html_text, options, exp = item
            # Extract digits using regex
            num_match = re.search(r'(\d+)', html_text)
            if not num_match:
                # Map circled numbers
                circle_map = {'①':1,'②':2,'③':3,'④':4,'⑤':5,'⑥':6,'⑦':7,'⑧':8,'⑨':9,'⑩':10,
                              '⑪':11,'⑫':12,'⑬':13,'⑭':14,'⑮':15,'⑯':16,'⑰':17,'⑱':18,'⑲':19,'⑳':20,
                              '㉑':21,'㉒':22,'㉓':23,'㉔':24,'㉕':25,'㉖':26,'㉗':27,'㉘':28,'㉙':29,'㉚':30,
                              '㉛':31,'㉜':32,'㉝':33,'㉞':34,'㉟':35,'㊱':36,'㊲':37,'㊳':38,'㊴':39,'㊵':40,
                              '㊶':41,'㊷':42,'㊸':43,'㊹':44,'㊺':45,'㊻':46,'㊼':47,'㊽':48,'㊾':49,'㊿':50}
                for c, n in circle_map.items():
                    if c in html_text:
                        num = n
                        break
            else:
                num = int(num_match.group(1))

            ans_choice = raw_answer_key[num]
            ans_idx = ans_choice - 1 # 0-indexed

            q_obj = {
                "id": f"q_{sec_id}_{num}",
                "num": num,
                "sectionId": sec_id,
                "sectionTitle": sec_title,
                "rubyHtml": html_text,
                "options": options,
                "answer": ans_idx,
                "explanation": exp
            }
            res.append(q_obj)
        else:
            num = item["num"]
            ans_choice = raw_answer_key[num]
            ans_idx = ans_choice - 1

            q_obj = {
                "id": f"q_{sec_id}_{num}",
                "num": num,
                "sectionId": sec_id,
                "sectionTitle": sec_title,
                "passageHtml": item.get("passageHtml"),
                "rubyHtml": item["rubyHtml"],
                "options": item["options"],
                "answer": ans_idx,
                "explanation": item["explanation"]
            }
            res.append(q_obj)
    return res

def main():
    vocab_q = build_questions("vocab", "Language Knowledge (Vocabulary)", vocab_questions_data)
    grammar_q = build_questions("grammar", "Language Knowledge (Grammar & Particles)", grammar_questions_data)
    reading_q = build_questions("reading", "Reading Comprehension (読解)", reading_questions_data)

    dataset = {
        "id": "jlpt-n5-mock-test-2",
        "title": "JLPT N5 Official Mock Examination Set 2",
        "level": "N5",
        "timeLimitMinutes": 50,
        "passingScore": 80,
        "maxScore": 180,
        "sections": [
            {
                "id": "vocab",
                "title": "Language Knowledge (Vocabulary)",
                "weight": 50,
                "questions": vocab_q
            },
            {
                "id": "grammar",
                "title": "Language Knowledge (Grammar)",
                "weight": 70,
                "questions": grammar_q
            },
            {
                "id": "reading",
                "title": "Reading Comprehension",
                "weight": 60,
                "questions": reading_q
            }
        ]
    }

    out_path = r"c:\Users\Administrator\Pictures\mock test\data\n5_mock_test_2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"🎉 Generated {len(vocab_q)+len(grammar_q)+len(reading_q)} questions into {out_path}")

if __name__ == "__main__":
    main()
