#!/usr/bin/env python3
"""
Generate comprehensive JLPT N5 Japanese Particle Mock Exam with 100% complete HTML Furigana readings
"""

import json
import os
import sys
import re

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Comprehensive 40 JLPT N5 Particle Questions with HTML Furigana (<ruby>漢字<rt>かんじ</rt></ruby>)

questions = [
    # SECTION 1: Basic Subject, Topic & Object Markers (は・が・を・に・で)
    {
        "id": "q_part_1",
        "num": 1,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "① <ruby>私<rt>わたし</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>日本語<rt>にほんご</rt></ruby><ruby>学校<rt>がっこう</rt></ruby>の <ruby>学生<rt>がくせい</rt></ruby>です。",
        "options": ["1 は", "2 が", "3 を", "4 で"],
        "answer": 0,
        "explanation": "Particle 【は】 marks the topic of the sentence ('As for me...'). 私(わたし)は学生(がくせい)です。"
    },
    {
        "id": "q_part_2",
        "num": 2,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "② <ruby>毎朝<rt>まいあさ</rt></ruby> パン<span class=\"highlight-target\">（　）</span> <ruby>食<rt>た</rt></ruby>べます。",
        "options": ["1 に", "2 で", "3 を", "4 は"],
        "answer": 2,
        "explanation": "Particle 【を】 marks the direct object of the verb 食べます (to eat). パンを食べます。"
    },
    {
        "id": "q_part_3",
        "num": 3,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "③ <ruby>部屋<rt>へや</rt></ruby>に <ruby>猫<rt>ねこ</rt></ruby><span class=\"highlight-target\">（　）</span> います。",
        "options": ["1 が", "2 を", "3 で", "4 へ"],
        "answer": 0,
        "explanation": "Particle 【が】 marks the subject of existence with います/あります. 猫(ねこ)がいます。"
    },
    {
        "id": "q_part_4",
        "num": 4,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "④ <ruby>図書館<rt>としょかん</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>本<rt>ほん</rt></ruby>を <ruby>読<rt>よ</rt></ruby>みます。",
        "options": ["1 に", "2 で", "3 を", "4 から"],
        "answer": 1,
        "explanation": "Particle 【で】 indicates the location where an action takes place. 図書館(としょかん)で読みます。"
    },
    {
        "id": "q_part_5",
        "num": 5,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑤ <ruby>公園<rt>こうえん</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>綺麗<rt>きれい</rt></ruby>な <ruby>花<rt>はな</rt></ruby>が あります。",
        "options": ["1 に", "2 で", "3 を", "4 へ"],
        "answer": 0,
        "explanation": "Particle 【に】 indicates the static location of existence (あります). 公園(こうえん)にあります。"
    },
    {
        "id": "q_part_6",
        "num": 6,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑥ <ruby>私<rt>わたし</rt></ruby>は <ruby>音楽<rt>おんがく</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>好<rt>す</rt></ruby>きです。",
        "options": ["1 を", "2 が", "3 に", "4 で"],
        "answer": 1,
        "explanation": "Adjectives of preference/ability like 好き (like), 上手 (good at), 欲しい (want) take 【が】. 音楽(おんがく)が好きです。"
    },
    {
        "id": "q_part_7",
        "num": 7,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑦ <ruby>喉<rt>のど</rt></ruby>が <ruby>乾<rt>かわ</rt></ruby>いたので、<ruby>水<rt>みず</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>飲<rt>の</rt></ruby>みたいです。",
        "options": ["1 が", "2 で", "3 へ", "4 に"],
        "answer": 0,
        "explanation": "The ~たい (want to do) form takes either 【が】 or 【を】. Here 【が】 is the correct option. 水(みず)が飲みたいです。"
    },
    {
        "id": "q_part_8",
        "num": 8,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑧ <ruby>日本語<rt>にほんご</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>分<rt>わ</rt></ruby>かりますか。",
        "options": ["1 を", "2 が", "3 で", "4 に"],
        "answer": 1,
        "explanation": "The verb 分かる (understand) marks its target object with 【が】. 日本語(にほんご)が分かりますか。"
    },
    {
        "id": "q_part_9",
        "num": 9,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑨ <ruby>机<rt>つくえ</rt></ruby>の <ruby>上<rt>うえ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>辞書<rt>じしょ</rt></ruby>を <ruby>置<rt>お</rt></ruby>きました。",
        "options": ["1 に", "2 で", "3 を", "4 へ"],
        "answer": 0,
        "explanation": "Particle 【に】 specifies the target place where something is placed or put (置く). 机(つくえ)の上に置く。"
    },
    {
        "id": "q_part_10",
        "num": 10,
        "sectionId": "basic_particles",
        "sectionTitle": "Basic Markers (は・が・を・に・で)",
        "rubyHtml": "⑩ <ruby>昨日<rt>きのう</rt></ruby> デパート<span class=\"highlight-target\">（　）</span> <ruby>靴<rt>くつ</rt></ruby>を <ruby>買<rt>か</rt></ruby>いました。",
        "options": ["1 に", "2 で", "3 へ", "4 が"],
        "answer": 1,
        "explanation": "Particle 【で】 marks the location of the action 買いました (bought). デパートで買いました。"
    },

    # SECTION 2: Time, Motion, Means & Direction (に・で・へ・から・まで)
    {
        "id": "q_part_11",
        "num": 11,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑪ <ruby>毎朝<rt>まいあさ</rt></ruby> <ruby>七時<rt>しちじ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>起<rt>お</rt></ruby>きます。",
        "options": ["1 に", "2 で", "3 を", "4 へ"],
        "answer": 0,
        "explanation": "Particle 【に】 marks a specific clock time or calendar date. 七時(しちじ)に起きます。"
    },
    {
        "id": "q_part_12",
        "num": 12,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑫ <ruby>明日<rt>あした</rt></ruby> <ruby>東京<rt>とうきょう</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>行<rt>い</rt></ruby>きます。",
        "options": ["1 へ", "2 で", "3 を", "4 から"],
        "answer": 0,
        "explanation": "Particle 【へ】 (pronounced 'e') or 【に】 indicates destination of motion verbs like 行きます, 来ます, 帰ります."
    },
    {
        "id": "q_part_13",
        "num": 13,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑬ <ruby>電車<rt>でんしゃ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>学校<rt>がっこう</rt></ruby>へ <ruby>通<rt>かよ</rt></ruby>っています。",
        "options": ["1 に", "2 で", "3 を", "4 から"],
        "answer": 1,
        "explanation": "Particle 【で】 marks the means of transportation or tool. 電車(でんしゃ)で行きます/通います。"
    },
    {
        "id": "q_part_14",
        "num": 14,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑭ <ruby>会議<rt>かいぎ</rt></ruby>は <ruby>九時<rt>くじ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>始<rt>はじ</rt></ruby>まります。",
        "options": ["1 から", "2 まで", "3 で", "4 を"],
        "answer": 0,
        "explanation": "Particle 【から】 marks the starting time or origin point ('from 9 o'clock'). 九時(くじ)から。"
    },
    {
        "id": "q_part_15",
        "num": 15,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑮ <ruby>授業<rt>じゅぎょう</rt></ruby>は <ruby>五時<rt>ごじ</rt></ruby><span class=\"highlight-target\">（　）</span> です。",
        "options": ["1 から", "2 まで", "3 に", "4 で"],
        "answer": 1,
        "explanation": "Particle 【まで】 indicates the ending time or destination limit ('until 5 o'clock'). 五時(ごじ)まで。"
    },
    {
        "id": "q_part_16",
        "num": 16,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑯ <ruby>家<rt>うち</rt></ruby>から <ruby>駅<rt>えき</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>歩<rt>ある</rt></ruby>いて <ruby>十五分<rt>じゅうごふん</rt></ruby> かかります。",
        "options": ["1 まで", "2 に", "3 へ", "4 で"],
        "answer": 0,
        "explanation": "The pair 【から...まで】 means 'from... to/until...'. 家(うち)から駅(えき)まで。"
    },
    {
        "id": "q_part_17",
        "num": 17,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑰ <ruby>箸<rt>はし</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>御飯<rt>ごはん</rt></ruby>を <ruby>食<rt>た</rt></ruby>べます。",
        "options": ["1 に", "2 で", "3 を", "4 と"],
        "answer": 1,
        "explanation": "Particle 【で】 denotes instrument/utensil used ('with chopsticks'). 箸(はし)で食べます。"
    },
    {
        "id": "q_part_18",
        "num": 18,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑱ <ruby>来年<rt>らいねん</rt></ruby>の <ruby>三月<rt>さんがつ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>国<rt>くに</rt></ruby>へ <ruby>帰<rt>かえ</rt></ruby>ります。",
        "options": ["1 に", "2 で", "3 を", "4 が"],
        "answer": 0,
        "explanation": "Specific time in the calendar takes 【に】. 三月(さんがつ)に帰ります。"
    },
    {
        "id": "q_part_19",
        "num": 19,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑲ <ruby>日本語<rt>にほんご</rt></ruby><span class=\"highlight-target\">（　）</span> レポートを <ruby>書<rt>か</rt></ruby>いて ください。",
        "options": ["1 で", "2 に", "3 を", "4 から"],
        "answer": 0,
        "explanation": "Particle 【で】 marks the language or medium used ('in Japanese'). 日本語(にほんご)で書いてください。"
    },
    {
        "id": "q_part_20",
        "num": 20,
        "sectionId": "motion_time",
        "sectionTitle": "Time, Motion & Means (に・で・へ・から・まで)",
        "rubyHtml": "⑳ <ruby>友達<rt>ともだち</rt></ruby><span class=\"highlight-target\">（　）</span> プレゼントを あげました。",
        "options": ["1 に", "2 で", "3 を", "4 へ"],
        "answer": 0,
        "explanation": "Particle 【に】 marks the recipient / indirect object of actions like あげる (give) or 教える (teach). 友達(ともだち)にあげる。"
    },

    # SECTION 3: Relational, Inclusive & Comparison Particles (の・と・や・より・も)
    {
        "id": "q_part_21",
        "num": 21,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉑ これは <ruby>私<rt>わたし</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>傘<rt>かさ</rt></ruby>です。",
        "options": ["1 の", "2 と", "3 に", "4 で"],
        "answer": 0,
        "explanation": "Possessive / Noun modification particle 【の】. 私(わたし)の傘(かさ) (my umbrella)."
    },
    {
        "id": "q_part_22",
        "num": 22,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉒ <ruby>日曜日<rt>にちようび</rt></ruby> <ruby>友達<rt>ともだち</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>映画<rt>えいが</rt></ruby>を <ruby>見<rt>み</rt></ruby>に<ruby>行<rt>い</rt></ruby>きました。",
        "options": ["1 と", "2 に", "3 で", "4 を"],
        "answer": 0,
        "explanation": "Particle 【と】 means 'together with' a person. 友達(ともだち)と行く。"
    },
    {
        "id": "q_part_23",
        "num": 23,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉓ かばんの <ruby>中<rt>なか</rt></ruby>に <ruby>本<rt>ほん</rt></ruby><span class=\"highlight-target\">（　）</span> ノートなどが あります。",
        "options": ["1 や", "2 と", "3 の", "4 も"],
        "answer": 0,
        "explanation": "Particle 【や】 is used for non-exhaustive lists ('books, notebooks, etc.'). 本(ほん)やノート。"
    },
    {
        "id": "q_part_24",
        "num": 24,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉔ <ruby>田中<rt>たなか</rt></ruby>さんも <ruby>鈴木<rt>すずき</rt></ruby>さん<span class=\"highlight-target\">（　）</span> <ruby>学生<rt>がくせい</rt></ruby>です。",
        "options": ["1 も", "2 は", "3 が", "4 と"],
        "answer": 0,
        "explanation": "Particle 【も】 means 'also / too'. 鈴木(すずき)さんも学生(がくせい)です。"
    },
    {
        "id": "q_part_25",
        "num": 25,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉕ <ruby>新幹線<rt>しんかんせん</rt></ruby>は <ruby>電車<rt>でんしゃ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>速<rt>はや</rt></ruby>いです。",
        "options": ["1 より", "2 ほう", "3 から", "4 まで"],
        "answer": 0,
        "explanation": "Particle 【より】 indicates standard of comparison ('faster than normal train'). 電車(でんしゃ)より速(はや)い。"
    },
    {
        "id": "q_part_26",
        "num": 26,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉖ りんご<span class=\"highlight-target\">（　）</span> みかんを <ruby>買<rt>か</rt></ruby>いました。",
        "options": ["1 と", "2 や", "3 の", "4 は"],
        "answer": 0,
        "explanation": "Complete list enumeration of 2 items takes 【と】. りんごとみかん。"
    },
    {
        "id": "q_part_27",
        "num": 27,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉗ <ruby>私<rt>わたし</rt></ruby>は <ruby>一回<rt>いっかい</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>富士山<rt>ふじさん</rt></ruby>に <ruby>登<rt>のぼ</rt></ruby>ったことが ありません。",
        "options": ["1 も", "2 は", "3 が", "4 に"],
        "answer": 0,
        "explanation": "Counter + 【も】 + negative verb means 'not even once'. 一回(いっかい)もありません。"
    },
    {
        "id": "q_part_28",
        "num": 28,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉘ <ruby>日本<rt>にほん</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>夏<rt>なつ</rt></ruby>は とても あついです。",
        "options": ["1 の", "2 で", "3 に", "4 と"],
        "answer": 0,
        "explanation": "Noun link / attribute particle 【の】. 日本(にほん)の夏(なつ) (Japan's summer)."
    },
    {
        "id": "q_part_29",
        "num": 29,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉙ コーヒー<span class=\"highlight-target\">（　）</span> <ruby>紅茶<rt>こうちゃ</rt></ruby>の <ruby>方<rt>ほう</rt></ruby>が <ruby>好<rt>す</rt></ruby>きですか。",
        "options": ["1 と", "2 や", "3 に", "4 より"],
        "answer": 0,
        "explanation": "In comparison question structure [A と B と どちら/ほう...], 【と】 links option choices."
    },
    {
        "id": "q_part_30",
        "num": 30,
        "sectionId": "relational_advanced",
        "sectionTitle": "Relational & Comparison Particles (の・と・や・より・も)",
        "rubyHtml": "㉚ <ruby>教室<rt>きょうしつ</rt></ruby>に <ruby>誰<rt>だれ</rt></ruby><span class=\"highlight-target\">（　）</span> いません。",
        "options": ["1 も", "2 が", "3 は", "4 に"],
        "answer": 0,
        "explanation": "Question word + 【も】 + negative verb means 'nobody' (誰(だれ)もいません)."
    },

    # SECTION 4: Conversational & Sentence Ending Particles (か・ね・よ・しか・など)
    {
        "id": "q_part_31",
        "num": 31,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㉛ A: 「お<ruby>国<rt>くに</rt></ruby>は どちらですか。」<br>B: 「アメリカです<span class=\"highlight-target\">（　）</span>。」",
        "options": ["1 か", "2 よ", "3 ね", "4 の"],
        "answer": 1,
        "explanation": "Sentence ending particle 【よ】 provides new information to the listener assertion."
    },
    {
        "id": "q_part_32",
        "num": 32,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㉢ <ruby>今日<rt>きょう</rt></ruby>は いい お<ruby>天気<rt>てんき</rt></ruby>ですね<span class=\"highlight-target\">（　）</span>。",
        "options": ["1 ね", "2 よ", "3 か", "4 わ"],
        "answer": 0,
        "explanation": "Sentence ending particle 【ね】 seeks agreement / confirmation ('isn't it?')."
    },
    {
        "id": "q_part_33",
        "num": 33,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㉝ <ruby>財布<rt>さいふ</rt></ruby>の <ruby>中<rt>なか</rt></ruby>に <ruby>百円<rt>ひゃくえん</rt></ruby><span class=\"highlight-target\">（　）</span> ありません。",
        "options": ["1 しか", "2 だけ", "3 も", "4 から"],
        "answer": 0,
        "explanation": "Pattern 【しか + negative verb】 means 'only / nothing but' (百円(ひゃくえん)しかありません)."
    },
    {
        "id": "q_part_34",
        "num": 34,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㉞ <ruby>喉<rt>のど</rt></ruby>が <ruby>渇<rt>かわ</rt></ruby>きましたね。お<ruby>茶<rt>ちゃ</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>飲<rt>の</rt></ruby>みましょうか。",
        "options": ["1 でも", "2 しか", "3 も", "4 より"],
        "answer": 0,
        "explanation": "Particle 【でも】 suggests an option loosely ('tea or something?'). お茶(ちゃ)でも。"
    },
    {
        "id": "q_part_35",
        "num": 35,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㉟ <ruby>一緒<rt>いっしょ</rt></ruby>に <ruby>映画<rt>えいが</rt></ruby>を <ruby>見<rt>み</rt></ruby>に<ruby>行<rt>い</rt></ruby>きませんか<span class=\"highlight-target\">（　）</span>。",
        "options": ["1 か", "2 よ", "3 ね", "4 を"],
        "answer": 0,
        "explanation": "Inviting structure ~ませんか takes question particle 【か】."
    },
    {
        "id": "q_part_36",
        "num": 36,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㊱ この テストは <ruby>十分<rt>じゅっぷん</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>終<rt>お</rt></ruby>わります。",
        "options": ["1 で", "2 に", "3 を", "4 から"],
        "answer": 0,
        "explanation": "Particle 【で】 denotes total time limit or boundary ('finish in 10 minutes'). 十分(じゅっぷん)で終わる。"
    },
    {
        "id": "q_part_37",
        "num": 37,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㊲ <ruby>父<rt>ちち</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>写真<rt>しゃしん</rt></ruby>を <ruby>撮<rt>と</rt></ruby>ってもらいました。",
        "options": ["1 に", "2 を", "3 で", "4 から"],
        "answer": 0,
        "explanation": "In ~てもらう (receive action), the agent performing the favor is marked by 【に】 (父(ちち)に撮ってもらう)."
    },
    {
        "id": "q_part_38",
        "num": 38,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㊳ <ruby>雨<rt>あめ</rt></ruby>が <ruby>降<rt>ふ</rt></ruby>っていますから、タクシー<span class=\"highlight-target\">（　）</span> <ruby>帰<rt>かえ</rt></ruby>りましょう。",
        "options": ["1 で", "2 に", "3 を", "4 へ"],
        "answer": 0,
        "explanation": "Transportation tool particle 【で】 (by taxi). タクシーで帰りましょう。"
    },
    {
        "id": "q_part_39",
        "num": 39,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㊴ A: 「この <ruby>本<rt>ほん</rt></ruby>は <ruby>誰<rt>だれ</rt></ruby>のてすか。」<br>B: 「わたし<span class=\"highlight-target\">（　）</span>です。」",
        "options": ["1 の", "2 は", "3 が", "4 に"],
        "answer": 0,
        "explanation": "Possessive pronoun drop: わたしの (mine). わたしのです。"
    },
    {
        "id": "q_part_40",
        "num": 40,
        "sectionId": "discourse_dialogue",
        "sectionTitle": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
        "rubyHtml": "㊵ <ruby>来週<rt>らいしゅう</rt></ruby>の <ruby>土曜日<rt>どようび</rt></ruby><span class=\"highlight-target\">（　）</span> <ruby>日曜日<rt>にちようび</rt></ruby>に <ruby>遊<rt>あそ</rt></ruby>びましょう。",
        "options": ["1 か", "2 と", "3 や", "4 に"],
        "answer": 0,
        "explanation": "Particle 【か】 means 'or' when joining two noun alternatives (Saturday or Sunday). 土曜日(どようび)か日曜日(にちようび)。"
    }
]

for q in questions:
    if "rubyHtml" in q and "text" not in q:
        clean_txt = re.sub(r'<rt>.*?</rt>', '', q["rubyHtml"])
        clean_txt = re.sub(r'<.*?>', '', clean_txt)
        q["text"] = clean_txt.strip()

quiz_data = {
    "id": "jlpt-n5-particles-exam",
    "title": "JLPT N5 Special Particle Master Examination (助詞特訓テスト)",
    "level": "N5",
    "timeLimitMinutes": 35,
    "passingScore": 80,
    "maxScore": 180,
    "sections": [
        {
            "id": "basic_particles",
            "title": "Basic Markers (は・が・を・に・で)",
            "weight": 45,
            "questions": [q for q in questions if q["sectionId"] == "basic_particles"]
        },
        {
            "id": "motion_time",
            "title": "Time, Motion & Means (に・で・へ・から・まで)",
            "weight": 45,
            "questions": [q for q in questions if q["sectionId"] == "motion_time"]
        },
        {
            "id": "relational_advanced",
            "title": "Relational & Comparison Particles (の・と・や・より・も)",
            "weight": 45,
            "questions": [q for q in questions if q["sectionId"] == "relational_advanced"]
        },
        {
            "id": "discourse_dialogue",
            "title": "Sentence-Ending & Context Particles (か・ね・よ・しか・など)",
            "weight": 45,
            "questions": [q for q in questions if q["sectionId"] == "discourse_dialogue"]
        }
    ]
}

output_path = r'c:\Users\Administrator\Pictures\mock test\data\n5_particles_furigana.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(questions)} particle questions dataset at data/n5_particles_furigana.json!")
