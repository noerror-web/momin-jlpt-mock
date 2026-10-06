#!/usr/bin/env python3
"""
Build Complete Authentic JLPT N5 Dataset for Website
Generates 52 Vocabulary Questions, 36 Grammar Questions, and 4 Reading Questions
with rich sentences, furigana/ruby HTML, target highlights, options, and explanations.
"""

import json
import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Answer Keys (1-indexed choice numbers: convert to 0-indexed for JSON answer)
vocab_ans_key = {
    1: 2, 2: 3, 3: 4, 4: 1, 5: 2, 6: 1, 7: 4, 8: 1, 9: 3, 10: 2,
    11: 3, 12: 4, 13: 2, 14: 3, 15: 1, 16: 2, 17: 1, 18: 3,
    19: 4, 20: 3, 21: 2, 22: 4, 23: 1, 24: 1, 25: 3, 26: 4, 27: 1, 28: 2, 29: 2, 30: 4,
    31: 2, 32: 4, 33: 3, 34: 4, 35: 2, 36: 1, 37: 2, 38: 1, 39: 3, 40: 1, 41: 4, 42: 3, 43: 3, 44: 1, 45: 1,
    46: 4, 47: 3, 48: 1, 49: 4, 50: 2, 51: 1, 52: 3
}

grammar_ans_key = {
    1: 2, 2: 4, 3: 3, 4: 2, 5: 1, 6: 2, 7: 3, 8: 4, 9: 3, 10: 4,
    11: 1, 12: 2, 13: 3, 14: 2, 15: 4, 16: 1, 17: 3, 18: 4, 19: 3, 20: 1,
    21: 3, 22: 2, 23: 3, 24: 4,
    25: 2, 26: 3, 27: 2, 28: 1, 29: 4, 30: 4, 31: 2,
    32: 3, 33: 1, 34: 4, 35: 3, 36: 4
}

reading_ans_key = {
    1: 4, 2: 3, 3: 2, 4: 2
}

# --- 52 VOCABULARY QUESTIONS ---
vocab_items_data = [
    # もんだい 1: Kanji Reading (Questions 1 - 18)
    ("① あの <span class=\"highlight-target\">先生</span>は わかいです。", ["1 せんせえ", "2 せんせい", "3 せんせん", "4 せんせ"], "先生 (せんせい) means teacher."),
    ("② あした えいがかんは <span class=\"highlight-target\">休み</span>です。", ["1 やつみ", "2 やづみ", "3 やすみ", "4 やずみ"], "休み (やすみ) means closed / holiday."),
    ("③ この セーターは <span class=\"highlight-target\">二千九百</span>えんでした。", ["1 にっせんきゅうひゃく", "2 にっせんくひゃく", "3 にせんきゅうびゃく", "4 にせんきゅうひゃく"], "二千九百 (にせんきゅうひゃく) = 2,900 yen."),
    ("④ すみません、<span class=\"highlight-target\">お金</span>を わすれました。", ["1 おかね", "2 おかぬ", "3 おがね", "4 おがぬ"], "お金 (おかね) means money."),
    ("⑤ まいにち <span class=\"highlight-target\">大学</span>へ いきます。", ["1 たいがく", "2 だいがく", "3 たいかく", "4 だいかく"], "大学 (だいがく) means university."),
    ("⑥ わたしは <span class=\"highlight-target\">雨</span>の 日が すきです。", ["1 あめ", "2 ゆき", "3 かぜ", "4 くも"], "雨 (あめ) means rain."),
    ("⑦ この <span class=\"highlight-target\">魚</span>は あたらしいです。", ["1 にく", "2 たまご", "3 やさい", "4 さかな"], "魚 (さかな) means fish."),
    ("⑧ あさって <span class=\"highlight-target\">友だち</span>が きます。", ["1 ともだち", "2 きょうだい", "3 かぞく", "4 りょうしん"], "友だち (ともだち) means friend."),
    ("⑨ <span class=\"highlight-target\">北</span>の ほうへ あるきましょう。", ["1 みなみ", "2 にし", "3 きた", "4 ひがし"], "北 (きた) means north."),
    ("⑩ 毎朝 <span class=\"highlight-target\">新聞</span>を よみます。", ["1 ざっし", "2 しんぶん", "3 ほん", "4 てがみ"], "新聞 (しんぶん) means newspaper."),
    ("⑪ 部屋の <span class=\"highlight-target\">電気</span>を つけて ください。", ["1 でんち", "2 てんき", "3 でんき", "4 でんしゃ"], "電気 (でんき) means electricity / light."),
    ("⑫ この <span class=\"highlight-target\">川</span>は とても ひろいです。", ["1 やま", "2 うみ", "3 いけ", "4 かわ"], "川 (かわ) means river."),
    ("⑬ 兄は <span class=\"highlight-target\">病院</span>で はたらいています。", ["1 びょうえん", "2 びょういん", "3 びよういん", "4 びようえん"], "病院 (びょういん) means hospital."),
    ("⑭ <span class=\"highlight-target\">外国人</span>の ともだちが います。", ["1 かいこくじん", "2 がいこくしん", "3 がいこくじん", "4 かいこくしん"], "外国人 (がいこくじん) means foreigner."),
    ("⑮ テーブルの うえに <span class=\"highlight-target\">本</span>が あります。", ["1 ほん", "2 き", "3 はやし", "4 もり"], "本 (ほん) means book."),
    ("⑯ わたしの <span class=\"highlight-target\">父</span>は 50さいです。", ["1 はは", "2 ちち", "3 あに", "4 おとうと"], "父 (ちち) means my father."),
    ("⑰ コップの <span class=\"highlight-target\">水</span>を のみます。", ["1 みず", "2 き", "3 ひ", "4 つち"], "水 (みず) means water."),
    ("⑱ <span class=\"highlight-target\">電車</span>で がっこうへ いきます。", ["1 じどうしゃ", "2 じてんしゃ", "3 でんしゃ", "4 ひこうき"], "電車 (でんしゃ) means train."),

    # もんだい 2: Hiragana to Kanji (Questions 19 - 30)
    ("⑲ わたしは <span class=\"highlight-target\">がくせい</span>です。", ["1 先生", "2 留学生", "3 校長", "4 学生"], "がくせい is written in Kanji as 学生."),
    ("⑳ きょうは <span class=\"highlight-target\">みずいろ</span>の シャツを きています。", ["1 赤色", "2 青色", "3 水色", "4 白色"], "みずいろ (sky blue) is written as 水色."),
    ("㉑ くるまで <span class=\"highlight-target\">いっしょに</span> いきます。", ["1 一書に", "2 一緒に", "3 一生に", "4 一所に"], "いっしょに (together) is written as 一緒に."),
    ("㉒ この <span class=\"highlight-target\">いぬ</span>は かわいいです。", ["1 猫", "2 鳥", "3 馬", "4 犬"], "いぬ (dog) is written as 犬."),
    ("㉓ 毎朝 6時に <span class=\"highlight-target\">おきます</span>。", ["1 起きます", "2 行きます", "3 来ます", "4 帰ります"], "おきます (wake up) is written as 起きます."),
    ("㉔ <span class=\"highlight-target\">ひろい</span> 公園で あそびました。", ["1 広い", "2 狭い", "3 高い", "4 安い"], "ひろい (spacious/wide) is written as 広い."),
    ("㉕ 友だちと <span class=\"highlight-target\">はなし</span>ます。", ["1 聞き", "2 読み", "3 話し", "4 書き"], "はなします (talk) comes from 話す."),
    ("㉖ <span class=\"highlight-target\">ひだり</span>へ まがって ください。", ["1 右", "2 上", "3 下", "4 左"], "ひだり (left) is written as 左."),
    ("㉗ この <span class=\"highlight-target\">はな</span>は きれいです。", ["1 花", "2 木", "3 草", "4 竹"], "はな (flower) is written as 花."),
    ("㉘ <span class=\"highlight-target\">あおい</span> 空が みえます。", ["1 赤い", "2 青い", "3 白い", "4 黒い"], "あおい (blue) is written as 青い."),
    ("㉙ くだものを <span class=\"highlight-target\">かい</span>ました。", ["1 売り", "2 買い", "3 貸し", "4 借り"], "かいました (bought) comes from 買う."),
    ("㉚ <span class=\"highlight-target\">あした</span>の てんきは はれです。", ["1 昨日", "2 今日", "3 明後日", "4 明日"], "あした (tomorrow) is written as 明日."),

    # もんだい 3: Contextual Vocabulary Insertion (Questions 31 - 45)
    ("㉛ あついですね。<span class=\"highlight-target\">（　）</span>を のみましょう。", ["1 くすり", "2 つめたい みず", "3 ごはん", "4 えんぴつ"], "Drinking cold water (つめたい みず) fits best when hot."),
    ("㉢ <span class=\"highlight-target\">（　）</span>が いたいので、病院へ いきます。", ["1 くつ", "2 かばん", "3 メガネ", "4 あたま"], "Headache (あたまが いたい) is a reason to go to hospital."),
    ("㉝ 部屋が くらいですから、ランプを <span class=\"highlight-target\">（　）</span>で ください。", ["1 けして", "2 あけて", "3 つけて", "4 しめて"], "Turn on (つけて) the light when it is dark."),
    ("㉞ 荷物が おもいですから、<span class=\"highlight-target\">（　）</span> もちましょう。", ["1 ひとりで", "2 ゆっくり", "3 まだ", "4 いっしょに"], "Carry together (いっしょに) because it is heavy."),
    ("㉟ バスに のって、がっこうの まえで <span class=\"highlight-target\">（　）</span>ました。", ["1 のり", "2 おり", "3 すわり", "4 たち"], "Got off (おりました) the bus."),
    ("㊱ 毎朝 7時に <span class=\"highlight-target\">（　）</span>を 食べてから、会社へ 行きます。", ["1 朝ごはん", "2 晩ごはん", "3 おやつ", "4 昼ごはん"], "Eating breakfast (朝ごはん) in the morning."),
    ("㊲ <span class=\"highlight-target\">（　）</span>を かいて、手紙を ポストに いれました。", ["1 きっぷ", "2 じゅうしょ", "3 しんぶん", "4 かさ"], "Writing address (じゅうしょ) on a letter."),
    ("㊳ <span class=\"highlight-target\">（　）</span>ですから、コートを きてください。", ["1 さむい", "2 あつい", "3 すずしい", "4 あたたかい"], "Put on a coat because it is cold (さむい)."),
    ("㊴ この くつは <span class=\"highlight-target\">（　）</span>ですから、あるきやすいです。", ["1 おもい", "2 かたい", "3 かるい", "4 ながい"], "Shoes are light (かるい), making walking easy."),
    ("㊵ えいごの <span class=\"highlight-target\">（　）</span>を よみます。", ["1 じしょ", "2 とけい", "3 カレンダー", "4 カメラ"], "Reading an English dictionary (じしょ)."),
    ("㊱ テーブルの うえを <span class=\"highlight-target\">（　）</span>に しました。", ["1 くろい", "2 ひろい", "3 きたない", "4 きれい"], "Cleaned / tidied (きれい) the tabletop."),
    ("㊲ がっこうの あとで、図書館で <span class=\"highlight-target\">（　）</span>を しました。", ["1 そうじ", "2 さんぽ", "3 べんきょう", "4 かいもの"], "Studied (べんきょう) at the library."),
    ("㊳ あの 店の ケーキは <span class=\"highlight-target\">（　）</span>て おいしいです。", ["1 からい", "2 しょっぱい", "3 あまい", "4 にがい"], "Cake is sweet (あまい) and delicious."),
    ("㊴ 時間が ありませんから、<span class=\"highlight-target\">（　）</span> あるきましょう。", ["1 はやく", "2 ゆっくり", "3 だんだん", "4 はじめて"], "Walk quickly (はやく) due to lack of time."),
    ("㊵ エレベーターが ありませんから、<span class=\"highlight-target\">（　）</span>で 上がります。", ["1 かいだん", "2 ドア", "3 窓", "4 天井"], "Going up using stairs (かいだん)."),

    # もんだい 4: Paraphrases / Similar Meaning (Questions 46 - 52)
    ("㊶ わたしは <span class=\"highlight-target\">デパート</span>へ いきました。", ["1 大きい 公園です", "2 本屋です", "3 病院です", "4 いろいろな 物を 売る 大きい 店です"], "Department store (デパート) is a big shop selling various items."),
    ("㊷ 昨日は <span class=\"highlight-target\">がっこうを やすみました</span>。", ["1 がっこうへ 行きました", "2 がっこうを はじめました", "3 がっこうへ 行きませんでした", "4 がっこうを おわりました"], "やすみました (was absent) means did not go to school."),
    ("㊸ この 本は <span class=\"highlight-target\">おもしろい</span>です。", ["1 たのしいです", "2 むずかしいです", "3 つまらないです", "4 たかいです"], "おもしろい (fun/interesting) is similar in meaning to たのしい."),
    ("㊹ 部屋の なかを <span class=\"highlight-target\">そうじしました</span>。", ["1 くらくしました", "2 つめたくしました", "3 あたたかくしました", "4 きれいにしました"], "そうじしました (cleaned) means made clean (きれいにしました)."),
    ("㊺ この 人は わたしの <span class=\"highlight-target\">きょうだい</span>です。", ["1 友だちです", "2 兄や 弟です", "3 父や 母です", "4 先生です"], "きょうだい (siblings) refers to brothers / sisters."),
    ("㊻ <span class=\"highlight-target\">さ来年</span> 日本へ いきます。", ["1 2年あと", "2 1年あと", "3 今年", "4 去年"], "さ来年 (year after next) means 2 years later (2年あと)."),
    ("㊼ 田中さんは <span class=\"highlight-target\">背が 高い</span>です。", ["1 手が 長いです", "2 足が はやいです", "3 身長が 大きいです", "4 体が 小さいです"], "背が高い (tall height) means large stature (身長が大きい).")
]

# --- 36 GRAMMAR QUESTIONS ---
grammar_items_data = [
    # もんだい 1: Grammar & Particle Select (Questions 1 - 24)
    ("① わたしは 毎朝 7時<span class=\"highlight-target\">（　）</span> おきます。", ["1 を", "2 に", "3 で", "4 へ"], "Time particle に marks specific time (7時に)."),
    ("② 図書館<span class=\"highlight-target\">（　）</span> 日本語を 勉強します。", ["1 に", "2 を", "3 へ", "4 で"], "Action location particle で indicates location of activity."),
    ("③ あした 友だち<span class=\"highlight-target\">（　）</span> えいがを 見に 行きます。", ["1 から", "2 まで", "3 と", "4 に"], "Particle と indicates 'together with' someone."),
    ("④ この りんごは 1つ 100円<span class=\"highlight-target\">（　）</span>です。", ["1 に", "2 です", "3 で", "4 が"], "Unit price copula structure (100円です)."),
    ("⑤ 部屋に テーブル<span class=\"highlight-target\">（　）</span> いすが あります。", ["1 や", "2 でも", "3 から", "4 の"], "Particle や is used for non-exhaustive listing."),
    ("⑥ きのうは 雨が ふりました<span class=\"highlight-target\">（　）</span>、きょうは いい てんきです。", ["1 だから", "2 が", "3 ので", "4 から"], "Conjunctive particle が links contrasting statements ('rained BUT nice today')."),
    ("⑦ これは わたし<span class=\"highlight-target\">（　）</span> かばんです。", ["1 に", "2 を", "3 の", "4 が"], "Possessive particle の links owner to item."),
    ("⑧ がっこうまで バス<span class=\"highlight-target\">（　）</span> 行きます。", ["1 に", "2 を", "3 へ", "4 で"], "Transport particle で indicates means of travel (by bus)."),
    ("⑨ コーヒー<span class=\"highlight-target\">（　）</span> お茶を のみませんか。", ["1 の", "2 が", "3 か", "4 に"], "Particle か provides alternative option ('coffee OR tea?')."),
    ("⑩ 昨日は どこ<span class=\"highlight-target\">（　）</span> 行きませんでした。", ["1 に", "2 で", "3 か", "4 へも"], "どこへも + negative verb = didn't go anywhere."),
    ("⑪ 砂糖を <span class=\"highlight-target\">（　）</span> 入れますか。", ["1 どのくらい", "2 どこ", "3 どっち", "4 だれ"], "どのくらい asks 'how much quantity'."),
    ("⑫ すみません、ペンを <span class=\"highlight-target\">（　）</span> ください。", ["1 かりて", "2 かして", "3 あげて", "4 もらって"], "かしてください = Please lend me."),
    ("⑬ もう 宿題を <span class=\"highlight-target\">（　）</span>か。", ["1 します", "2 しません", "3 しました", "4 しなかった"], "もう (already) pairs with past tense (しました)."),
    ("⑭ テレビを <span class=\"highlight-target\">（　）</span>ながら、ごはんを たべます。", ["1 見る", "2 見", "3 見て", "4 見た"], "Verb stem + ながら indicates simultaneous actions."),
    ("⑮ その 映画は あまり <span class=\"highlight-target\">（　）</span>です。", ["1 おもしろい", "2 おもしろかった", "3 おもしろくて", "4 おもしろくない"], "あまり + negative form (おもしろくない)."),
    ("⑯ 部屋を <span class=\"highlight-target\">（　）</span> 掃除しました。", ["1 きれいに", "2 きれいな", "3 きれいで", "4 きれい"], "Na-adjective + に + verb (きれいに)."),
    ("⑰ 窓を <span class=\"highlight-target\">（　）</span>も いいですか。", ["1 あける", "2 あけた", "3 あけて", "4 あけない"], "V-て + もいいですか asks permission."),
    ("⑱ あしたは 雨が <span class=\"highlight-target\">（　）</span>でしょう。", ["1 ふり", "2 ふって", "3 ふった", "4 ふる"], "Dictionary verb + でしょう indicates prediction."),
    ("⑲ 荷物を <span class=\"highlight-target\">（　）</span>ましょうか。", ["1 もつ", "2 もって", "3 もち", "4 もちます"], "Verb stem + ましょうか offers assistance."),
    ("⑳ ここで 写真を <span class=\"highlight-target\">（　）</span>で ください。", ["1 とらない", "2 とって", "3 とり", "4 とる"], "V-ない + でください = Please do not take photos."),
    ("㉑ 田中さんは 今 電話を <span class=\"highlight-target\">（　）</span>います。", ["1 かける", "2 かけた", "3 かけて", "4 かけ"], "V-て + います indicates continuous action."),
    ("㉒ 昨日は 忙しくて、どこへも <span class=\"highlight-target\">（　）</span>。", ["1 行きました", "2 行きませんでした", "3 行きます", "4 行きません"], "Past negative statement (行きませんでした)."),
    ("㉓ この 公園は <span class=\"highlight-target\">（　）</span>て 静かです。", ["1 ひろい", "2 ひろいな", "3 ひろく", "4 ひろかった"], "I-adj te-form drops い adds くて (ひろくて)."),
    ("㉔ 病院へ 行く <span class=\"highlight-target\">（　）</span>に、薬を 買いました。", ["1 あと", "2 とき", "3 から", "4 まえ"], "Dictionary verb + まえに = Before doing."),

    # もんだい 2: Sentence Composition (Star Questions ★) (Questions 25 - 31)
    ("㉕ わたしは 日本語 __ __ ★ __ 好きです。", ["1 を", "2 が", "3 とても", "4 話すの"], "Correct sentence: わたしは 日本語を 話すの ★が とても 好きです。(Star position is 2: が)."),
    ("㉖ テーブルの うえに __ __ ★ __ あります。", ["1 が", "2 本", "3 ノート", "4 と"], "Correct sentence: テーブルの うえに 本 と ★ノート が あります。(Star position is 3: ノート)."),
    ("㉗ きのう 買った __ ★ __ __ おいしかった。", ["1 は", "2 ケーキ", "3 とても", "4 の"], "Correct sentence: きのう 買った の ★ケーキ は とても おいしかった。(Star position is 2: ケーキ)."),
    ("㉘ あしたは 早く ★ __ __ __ 行けません。", ["1 起きないと", "2 から", "3 会社へ", "4 行かないと"], "Correct sentence: あしたは 早く ★起きないと 会社へ 行けません。(Star position is 1: 起きないと)."),
    ("㉙ 毎朝 __ __ __ ★ 新聞を よみます。", ["1 を", "2 のみながら", "3 コーヒー", "4 朝ごはんを"], "Correct sentence: 毎朝 コーヒー を のみながら ★朝ごはんを 食べて 新聞を よみます。(Star position is 4: 朝ごはんを)."),
    ("㉚ 駅の まえで __ __ __ ★ 会いました。", ["1 に", "2 昔の", "3 友だち", "4 たまたま"], "Correct sentence: 駅の まえで 昔の 友だち に ★たまたま 会いました。(Star position is 4: たまたま)."),
    ("㉛ 部屋が くらくなった __ ★ __ __ つけました。", ["1 つけました", "2 電気", "3 ので", "4 を"], "Correct sentence: 部屋が くらくなった ので ★電気 を つけました。(Star position is 2: 電気)."),

    # もんだい 3: Text Grammar Passage (Questions 32 - 36)
    ("【32】に はいる いちばん いい ものは どれですか。", ["1 会います", "2 会って", "3 会いました", "4 会う"], "Past tense verb 会いました (met) matches past narrative."),
    ("【33】に はいる いちばん いい ものは どれですか。", ["1 ふいていて", "2 ふきます", "3 ふいた", "4 ふかない"], "Te-form ふいていて connects wind state to cool feeling."),
    ("【34】に はいる いちばん いい ものは どれですか。", ["1 食べた", "2 食べる", "3 食べ", "4 食べて"], "Te-form 食べて links sequential actions."),
    ("【35】に はいる いちばん いい ものは どれですか。", ["1 しかし", "2 だから", "3 とても", "4 それから"], "Adverb とても (very) emphasizes enjoyable day."),
    ("【36】に はいる いちばん いい ものは どれですか。", ["1 どこか", "2 いつか", "3 だれか", "4 別の"], "別の (another / different) mountain to visit next time.")
]

# Passage for Grammar Questions 32-36
grammar_passage_html = """
<div style="background: rgba(99, 102, 241, 0.08); border-left: 4px solid #6366f1; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;">
  <strong>【文法 読解 本文】</strong><br>
  わたしは 先週の 日曜日に 友だちと 山へ 行きました。朝 7時に 駅で <strong>【32】</strong>。バスに 乗って 1時間くらいで 山の 入口に 着きました。山の上は 風が <strong>【33】</strong>、とても すずしかったです。みんなで お弁当を <strong>【34】</strong>、写真を とりました。帰りは 電車で 帰りました。<strong>【35】</strong> たのしい 一日でした。また <strong>【36】</strong> 山へ 行きたいです。
</div>
"""

# --- READING QUESTIONS ---
reading_questions_data = [
    {
        "id": "q_reading_1",
        "num": 1,
        "sectionId": "reading",
        "sectionTitle": "Reading Comprehension (読解)",
        "passageHtml": "<div style=\"background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;\"><strong>【読解 1】</strong><br>わたしは リーです。まいあさ 7じに おきます。あさごはんを たべてから、バスで がっこうへ いきます。がっこうは 9じから 3じまで です。きょうの ごごは としょかんで にほんごの べんきょうを しました。</div>",
        "rubyHtml": "問題 1: リーさんは きょうの ごご なにを しましたか。",
        "options": [
            "1 バスで がっこうへ いきました。",
            "2 7じに おきました。",
            "3 あさごはんを たべました。",
            "4 としょかんで にほんごの べんきょうを しました。"
        ],
        "answer": 3, # Choice 4
        "explanation": "Passage states: 'きょうの ごごは としょかんで にほんごの べんきょうを しました。'"
    },
    {
        "id": "q_reading_2",
        "num": 2,
        "sectionId": "reading",
        "sectionTitle": "Reading Comprehension (読解)",
        "passageHtml": "<div style=\"background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;\"><strong>【読解 2】</strong><br>田中さんの いえには かわいい 犬が 1ぴきと 猫が 2ひき います。毎朝 6時に 犬と さんぽを します。猫は いえの なかで ずっと ねています。</div>",
        "rubyHtml": "問題 2: 田中さんの いえに ペットは なんぴき いますか。",
        "options": [
            "1 1ぴき",
            "2 2ひき",
            "3 3びき",
            "4 4ひき"
        ],
        "answer": 2, # Choice 3
        "explanation": "1 dog + 2 cats = 3 animals (3びき)."
    },
    {
        "id": "q_reading_3",
        "num": 3,
        "sectionId": "reading",
        "sectionTitle": "Reading Comprehension (読解)",
        "passageHtml": "<div style=\"background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;\"><strong>【読解 3】</strong><br>木村さんは 毎週 土曜日に スーパ－へ 行って、一週間分の 食料品を 買います。日曜日には 部屋の 掃除と 洗濯を します。</div>",
        "rubyHtml": "問題 3: 木村さんは 日曜日に なにを しますか。",
        "options": [
            "1 スーパ－へ 行きます。",
            "2 掃除と 洗濯を します。",
            "3 会社へ 行きます。",
            "4 友だちと あそびます。"
        ],
        "answer": 1, # Choice 2
        "explanation": "Passage states: '日曜日には 部屋の 掃除と 洗濯を します。'"
    },
    {
        "id": "q_reading_4",
        "num": 4,
        "sectionId": "reading",
        "sectionTitle": "Reading Comprehension (読解)",
        "questionImage": "public/n5_diagrams/reading_page_46.png",
        "passageHtml": "<div style=\"background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 8px; font-size: 1.05rem; line-height: 1.8;\"><strong>【情報検索】</strong><br>下のお知らせを 見て、質問に 答えて ください。</div>",
        "rubyHtml": "問題 4: 図書館の 休館日は いつですか。お知らせを 見て えらんで ください。",
        "options": [
            "1 毎週 月曜日",
            "2 毎週 火曜日と 毎月 最終水曜日",
            "3 毎週 日曜日",
            "4 毎日"
        ],
        "answer": 1, # Choice 2
        "explanation": "Information Retrieval: Closed on Tuesdays and the last Wednesday of the month."
    }
]

def build_questions_list(sec_id, sec_title, items_data, ans_key_dict, passage_html=None):
    questions = []
    for idx, (html_text, options, explanation) in enumerate(items_data, start=1):
        correct_choice_1indexed = ans_key_dict[idx]
        ans_idx = correct_choice_1indexed - 1

        q_obj = {
            "id": f"q_{sec_id}_{idx}",
            "num": idx,
            "sectionId": sec_id,
            "sectionTitle": sec_title,
            "rubyHtml": html_text,
            "options": options,
            "answer": ans_idx,
            "explanation": explanation
        }

        # Attach grammar passage for grammar questions 32 to 36
        if sec_id == "grammar" and idx >= 32:
            q_obj["passageHtml"] = grammar_passage_html

        questions.append(q_obj)
    return questions

def main():
    vocab_questions = build_questions_list("vocab", "Language Knowledge (Vocabulary)", vocab_items_data, vocab_ans_key)
    grammar_questions = build_questions_list("grammar", "Language Knowledge (Grammar)", grammar_items_data, grammar_ans_key)
    
    quiz_dataset = {
        "id": "jlpt-n5-mock-exam-set",
        "title": "JLPT N5 Full Practice Examination",
        "level": "N5",
        "timeLimitMinutes": 50,
        "passingScore": 80,
        "maxScore": 180,
        "sections": [
            {
                "id": "vocab",
                "title": "Language Knowledge (Vocabulary)",
                "weight": 60,
                "questions": vocab_questions
            },
            {
                "id": "grammar",
                "title": "Language Knowledge (Grammar)",
                "weight": 60,
                "questions": grammar_questions
            },
            {
                "id": "reading",
                "title": "Reading Comprehension",
                "weight": 60,
                "questions": reading_questions_data
            }
        ]
    }

    out_file = r'c:\Users\Administrator\Pictures\mock test\data\n5_practice_set_9.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(quiz_dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully generated all 92 questions ({len(vocab_questions)} Vocab, {len(grammar_questions)} Grammar, {len(reading_questions_data)} Reading) into {out_file}!")

if __name__ == '__main__':
    main()
