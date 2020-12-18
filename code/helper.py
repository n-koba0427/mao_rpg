import numpy as np
import random
from search import Astar

#マップ
collision = [
    [#マップ１
        'xxxxxxxxxxgxxxxxxx',
        'xxxxx1111x01111x1x',
        'xx00x1111101x11x1x',
        'xxx0xkx111000x111x',
        'x1x0xxxx1x0x00xxxx',
        'x1x000xx1x0xx000xx',
        'x1xxx0xxxx0xxxx0sx',
        'g111x00000001xxxxx',
        'x11xx0xxxxxx11xxxx',
        'x11xx0xxxxxxxxxxxx',
        'x1xxx0xxxxxxxxx11x',
        'x0xxx0xxx11xxd111x',
        'x0xxx0x111xxxxxx1x',
        'x111x0xxx1xxx0001x',
        'x11x0000000000xx1x',
        'xx100111xxxxxxx11x',
        'xxs0xxxxxxx111111x',
        'xxxxxxxxxxxxxxxxxx',
    ],
    [#マップ２
        'xxxxxxxxxxxxxxxxxx',
        'xx111111111111111x',
        'xxx1111111xxxx111x',
        'x11111111xxxxxx11x',
        'x1xxxx0x11xxxx111x',
        'x1xxxx0x111111111x',
        'xxxxxx0xxxxx11111x',
        'xxxxxx0xxxxx11111x',
        'xxxxxx0xxxxxxx0x1x',
        'x1xxxx0xxxxxx000xx',
        'x1x11x00xxxx00x11x',
        'x11110000xx00xx11x',
        'x1111xxx0000xxxx1x',
        'x1111xxxxx0xxxxx1x',
        'xxx11xxxxx0xxxxx1x',
        'xxxx11x1xx001xx11x',
        'xxx111111x0x11111x',
        'xxxxxxxxxxgxxxxxxx',
    ],
    [#マップ３
        'xxxxxxxggxxxxxxxxx',
        'xxxxxxx00xxxxxxxxx',
        'xxxxxxx0xxxxxxxxxx',
        'xxxxxxx0xxx00000xx',
        'xxx000x0xxx0xxxmxx',
        'xxx0x0x00xx0xxxxxx',
        'xx00xexx0xx0xxxxxx',
        'xx0xxxx00xx000000g',
        'xx0xxxx0xxxxx0xxxx',
        'xx000000xxxkx0xxxx',
        'xxxx0xxxxx00x0xxxx',
        'xxxx0xxxx000x0xxxx',
        'xxxx0xxxx0xxx0xxxx',
        'xxxx0xxxx0xxx0xxxx',
        'xxxx0000000000xxxx',
        'xxxxxxxxxxxxxxxxxx',
        'xxxxxxxxxxxxxxxxxx',
    ],
    [#マップ４
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxxxxxxxxxxx",
        "xxxxxxxxMxxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxxx0xxxxxxxxx",
        "xxxxxxx00xxxxxxxxx",
        "xxxxxxxggxxxxxxxxx"
    ],
    # [#マップ４
    #     'xxxxxxxxxxxxxxxxxx',
    #     'xxxxx220022xxxxxxx',
    #     'xxx2200000022xxxxx',
    #     'xx22000xx00022xxxx',
    #     'xx22000xx00022xxxx',
    #     'xx2x20000002x2xxxx',
    #     'xx2x2x20M2x2x2xxxx',
    #     'xxx22x2002x22xxxxx',
    #     'xxxx22200222xxxxxx',
    #     'xxxxx220022xxxxxxx',
    #     'xxxxxx2002xxxxxxxx',
    #     'xxxxxxx00xxxxxxxxx',
    #     'xxxxxxx00xxxxxxxxx',
    #     'xxxxxxx00xxxxxxxxx',
    #     'xxxxxxx00xxxxxxxxx',
    #     'xxxxxxxggxxxxxxxxx',
    # ],
]

def get_tile_detail(m=0):
    return collision[m]

def strlist_editer(strlist, x, y, nward):
    strlist[y] = strlist[y][:x]+nward+strlist[y][x+1:]

def make_map():
    copy = collision
    for m in range(len(copy)):
        for y in range(len(copy[m])):
            for x in range(len(copy[m][y])):
                if copy[m][y][x] == '1':
                    strlist_editer(copy[m],x,y,random.choice(['i','m','0']))
                if copy[m][y][x] == '0':
                    strlist_editer(copy[m],x,y,random.choice(['p','0', '0', '0']))
    return copy

def convert_value_map(item_map, start, s_level, i_level, m):
    copy = item_map
    vmap = []
    astar = Astar(wall_code=['x', 'g'])
    astar2 = Astar(wall_code=['x'])
    max_value = [-1, []]
    for y in range(len(copy[m])):
        vmap.append([])
        for x in range(len(copy[m][y])):
            tile = copy[m][y][x]
            d = 0
            if not(tile == 'x' or tile == '0' or tile == '2'):
                if tile == 'g':
                    astar2.forward(copy[m], start, [x,y])
                    d = astar2.get_detail()['distance']
                    v = 2
                else:
                    astar.forward(copy[m], start, [x,y])
                    d = astar.get_detail()['distance']
                    if tile == 's':
                        v = s_level*2-1
                    elif tile == 'i':
                        v = i_level*2-2
                    elif tile == 'k' or tile == 'e' or tile == 'd':
                        v = 9
                    elif tile == 'm':
                        v = 3
                    elif tile == 'E':
                        v = 6
                    elif tile == 'p':
                        v = 1
            v = int(v/d*100) if not d == 0 else 0
            if v > max_value[0]:
                max_value = [v, [x,y]]
            vmap[y].append(v)
    #astar.show_result(use_ansi_esc=True)
    return vmap, max_value

#文字
f_list = [
    [
        'あいうえお',
        'かきくけこ',
        'さしすせそ',
        'たちつてと',
        'なにぬねの',
        'はひふへほ',
        'まみむめも',
        'や！ゆ？よ',
        'らりるれろ',
        'わ、を。ん',
        'っゃゅょー',
        '　＄ｓ/：',
        '０１２３４',
        '５６７８９',
        '01234',
        '56789',
    ],
    [
        'アイウエオ',
        'カキクケコ',
        'サシスセソ',
        'タチツテト',
        'ナニヌネノ',
        'ハヒフヘホ',
        'マミムメモ',
        'ヤｐユｂヨ',
        'ラリルレロ',
        'ワ＊ヲ＊ン',
        'ッャュョ＊',
    ]
]
def make_code(text):
    result = []
    for f in text:
        for R in range(len(f_list)):
            for r in range(len(f_list[R])):
                for c in range(5):
                    if f_list[R][r][c] == f:
                        result.append([72+r*8,R*40+c*8])
    return result

#文章
sentences = [
    [#0 最初
        'まおうさま　たいへんて、す！',
        'ゆうしゃか、うまれました！'
    ],
    [#1 魔王フェーズ
        'いそいて、モンスターたちを！！',
        'モンスターをなか、おして、しょうかんて、きま',
        'す！',
    ],
    [#2スライム　デフォ
        'しょうかんコスト　１　３　　５',
        'たいりょく　　　　５　１１　１７',
        'こうけ、きりょく　２　４　　６',
    ],
    [#3スケルトン　追加攻撃
        'しょうかんコスト　１　３　　５',
        'たいりょく　　　　５　１１　１７',
        'こうけ、きりょく　２　４　　６',
    ],
    [#4犬　先制攻撃
        'しょうかんコスト　１　３　　５',
        'たいりょく　　　　５　１１　１７',
        'こうけ、きりょく　２　４　　６',
    ],
    [#5 最初
        'ゆうしゃは１にち５マスすすめます',
        'まおうさまは１にち３コストつかえます',
    ],
    [#6 最初
        'うわああああ',
        'ゆうしゃか、たひ、をはし、めました！！',
        'あいつつよいアイテムをさか、しています！'
    ],
    [#7 e1
        'たいへんて、す！　ゆ　ゆうしゃがあああ',
        'エクスカリハ、ーをてにいれました！！',
    ],
    [#8 e2
        'エクスカリハ、ー',
        'こうけ、きりょくか、５あか、る',
    ],
    [#9 無言用
    ],
    [#10 日にち変更
        'まおうさまおきてくた、さい！！',
        'ゆうしゃはきょうもたひ、をすすめてます！',
    ],
    [#11 m
        'ゆうしゃはこせ、にをひろったようて、す',
        'ゆうしゃは＄１をケ、ットした',
    ],
    [#12 i
        'ゆうしゃはいやしスホ。ットをみつけました',
        'ゆうしゃのたいりょくか、２かいふく',
    ],
    [#13 0
        'ゆうしゃはとくになにもみつけなかった',
        'ラッキー！！',
    ],
    [#14 d1
        'たたたたいへんて、すまおうさま！！',
    ],
    [#15 d2
        'ゆ　ゆうしゃか、',
        'タ、イヤモント、をみつけました',
    ],
    [#16 d3
        'ゆうしゃはおおか、ねもちになった'
    ],
    [#17 s
        'ゆうしゃはショッフ。をおとす、れました',
    ],
    [#18 s(1)
        '＄２て、ハ、ント、エイト、をかった',
        '２のシールト、をかくとく',
    ],
    [#19 s(2)
        '＄４て、きす、く、すりをかった',
        '４のシールト、をかくとく',
    ],
    [#20 s(3)
        '＄６て、ホ。ーションをかった',
        '６のシールト、をかくとく',
    ],
    [#21 s(4-1)
        '＄８て、ハイエリクサーをかった',
        '８のシールト、をかくとく',
    ],
    [#22 s(5)
        '＄１０て、みか、わりにんき、ょうをかった',
        '１０のシールト、をかくとく',
    ],
    [#23 s(4-2)
        'レヘ、ル４のショッフ。',
        'てつのけんをかった',
        'こうけ、きりょく３アッフ。',
    ],
    [#24 k1
        'んんんんん？？',
        'ゆうしゃか、なんかみつけたみたいて、す',
    ],
    [#25 k2
        'あ！あれは！！',
        'すっこ、いて、っかいきのこて、す！！！',
    ],
    [#26 k3
        'たいりょうのけいけんちをケ、ット',
        'ゆうしゃのレヘ、ルが１あか、った',
    ],
    [#27 最初
        'マッフ。はやし、るして、いと、うできます',
    ],
    [#28 始まりの町
        '',
        'ゆうしゃははし、まりのまちにきた',
    ],
    [#29 呪いのもり
        '',
        'ゆうしゃはのろいのもりにきた',
    ],
    [#30 洞窟
        '',
        'ゆうしゃはと、うくつにきた',
    ],
    [#31 魔王城
        '',
        'ゆうしゃはまおうし、ょうにきた',
    ],
    [#32 保存案内
        'やし、るしキーて、テ、ータをせんたく',
        '',
        'ｓ：ほそ、ん　ｐ：あそふ、　ｂ：もと、る',
    ],
    [#33 最初
        'テ、ータのほそ、んはｓキーて、て、きます',
    ],
    [#34 gameover1
        'ます、いて、すまおうさま！！！！',
        'あのゆうしゃすっこ、いつよいて、す！',
    ],
    [#35 gameover2
        '',
        'まおうさまか、もした、い４けいたいになったら・',    
    ],
    [#36 gameover3
        'た、　た、めみたいて、す！かてません',
        'いそいて、にけ、ましょう！！',
    ],
    [#37 gameover4
        '',
        'まおうはゆうしゃをとめられなかった',    
    ],
    [#38 gameclear1
        '',
        'わっはっは　よくきたゆうしゃ！！', 
    ],
    [#39 gameclear2
        'まおうさま　こいつにはかてます！！',
        'やっちゃってくた、さい！！'
    ],
    [#40 gameclear3
        '',
        'まおうはゆうしゃをたおした', 
    ],
    [#41 城にモンスターを召喚した時のエラー
        'おしろにモンスターはしょうかんて、きません',
        '', 
    ],
    [#42 経験値
        'こ、みひろいをした',
        'ゆうしゃはけいけんちをかくとく', 
    ],
    [#43 経験値
        'きれいなはなをみつけた',
        'ゆうしゃはけいけんちをかくとく',  
    ],
    [#44 経験値
        'おいしいこ、はんをたへ、た',
        'ゆうしゃはけいけんちをかくとく', 
    ],
    [#45 経験値
        'すこしひるねをした',
        'ゆうしゃはけいけんちをかくとく', 
    ],
    [#46 保存メッセージ
        '',
        'テ、ータをほそ、んしました',
    ],
    [#47 最初
        'モンスターたちは',
        '１０にちて、レヘ、ルアッフ。します',
    ],
    [#48 モンスターがやられた
        '',
        'あああ　モンスターか、やられましたあ',
    ]
]
def get_sentence(n):
    result = []
    for s in sentences[n]:
        result.append(make_code(s))
    return result

if __name__ == '__main__':
    item_maps = make_map()
    for item_map in item_maps:
        for i in item_map:
            print(i)
        print(' ')

    value_map = convert_value_map(item_maps, [2,2], 1, 1, 0)
    for i in value_map[0]:
        print(i)
    print('max', value_map[1])