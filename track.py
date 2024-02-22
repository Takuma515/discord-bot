from typing import Optional

OFFSET = 4

def search(name: str) -> Optional[list]:
    name = str.lower(name)
    MKS = {'mks', 'マリオカートスタジアム', 'まりおかーとすたじあむ', 'マリカス', 'まりかす'}
    WP = {'wp', 'ウォーターパーク','うぉーたーぱーく', 'ウォタパ', 'うぉたぱ'}
    SSC = {'ssc', 'スイーツキャニオン', 'すいーつきゃにおん', 'スイキャニ', 'すいきゃに'}
    TR = {'tr', 'ドッスン遺跡', 'どっすんいせき', 'ドッスンいせき', 'ドッスンイセキ', 'ドッスン', 'どっすん', 'イセキ', 'いせき', '遺跡'}

    MC = {'mc', 'マリオサーキット', 'マリサ', 'まりおさーきっと', 'まりさ', '新マリサ', 'しんまりさ', 'シンマリサ', '新まりさ'}
    TH = {'th', 'キノピオハーバー', 'きのぴおはーばー', 'はーばー', 'ハーバー'}
    TM = {'tm', 'ねじれマンション', 'ねじれまんしょん', 'ねじまん', 'ねじマン', 'ネジマン', 'まんしょん', 'マンション', 'ねじれ', 'ネジレ', 'ねじ', 'ネジ'}
    SGF = {'sgf', 'へいほーこうざん', 'ヘイホー鉱山', 'ヘイホーこうざん', 'へいほー鉱山', 'へいこう', 'ヘイコウ', 'へい鉱', 'ヘイ鉱', 'ヘイこう', 'ヘイホー', 'へいほー'}

    SA = {'sa', 'サンシャイン空港', 'サンシャインくうこう', 'さんしゃいんくうこう', '空港', 'くうこう'}
    DS = {'ds', 'ドルフィンみさき', 'ドルフィン岬', 'どるふぃんみさき', 'どるふぃん岬', 'どるみ', 'ドルミ', 'どるふぃん', 'ドルフィン'}
    Ed = {'ed', 'エレドリ', 'エレド', 'エレクトロドリーム', 'えれどり', 'えれど', 'えれくとろどりーむ'}
    MW = {'mw', 'ワリオスノーマウンテン', 'わりおすのーまうんてん', 'ワリスノ', 'わりすの', '雪山', 'ゆきやまうんてん', 'すの', 'スノ'}

    CC = {'cc', 'スカイガーデン', 'スカガ', 'スカが', 'すかが',  'すかいがーでん'}
    BDD = {'bdd', 'ホネホネさばく', 'ホネホネ砂漠', 'ほねほねさばく', 'ほねほね砂漠', '骨骨砂漠', '骨骨さばく', 'ホネホネサバク', 'ほねさば', '骨サバ', 'ホネサバ', '骨', 'ほね', 'ホネ', 'ほねほね', '骨骨', 'ホネホネ'}
    BC = {'bc', 'クッパキャッスル', 'くっぱきゃっする', 'くっきゃぱっする', 'クッキャパッスル', 'くぱきゃ', 'クパキャ'}
    RR = {'rr', '新虹', '新にじ', 'しんにじ', 'レインボーロード', 'シンニジ', 'れいんぼーろーど'}

    rMMM = {'rmmm', 'mmm', 'モモカン', 'もーもーカントリー', 'モーモーカントリー', 'ももかん', 'もーもーかんとりー', '牛', 'うし'}
    rMC = {'rmc', 'gba', 'ぐばまり', 'グバマリ', 'ぐば', 'グバ', 'gbaまりさ', 'gbaマリサ', 'gbaマリオサーキット', 'gbaまりおさーきっと'}
    rCCB = {'rccb', 'ccb', 'プクプクビーチ', 'プクプク', 'プクビ', 'ぷくぷくびーち', 'ぷくぷく', 'ぷくび', 'びーち', 'ビーチ'}
    rTT = {'rtt', 'tt', 'キノピオハイウェイ', '高速道路', '高速', 'こうそくどうろ', 'こうそく', 'はいうぇい', 'ハイウェイ', 'きのぴおはいうぇい'}

    rDDD = {'rddd', 'カラカラ', 'カラサバ', 'からさば', 'からから', 'カラカラ砂漠', 'からからさばく', 'カラカラさばく', 'カラカラサバク'}
    rDP3 = {'rdp3', 'dp3', 'ドーナツへいや', 'どーなつへいや', 'ドーナツ平野', 'どーなつ平野', 'ドーナツヘイヤ', '平野', 'へいや'}
    rRRy = {'rrry', 'ピーチサーキット', 'ぴーちさーきっと', 'ピチさ', 'ピチサ', 'ぴちさ'}
    rDKJ = {'rdkj', 'dkj', 'dk', 'じゃんぐる', 'ジャングル'}

    rWS = {'rws', 'ws', 'ワリオスタジアム', 'ワリスタ', 'わりすた', 'わりおすたじあむ'}
    rSL = {'rsl', 'sl', 'しゃべらん', 'シャベラン', 'シャーベットランド', 'しゃーべっとらんど', 'シャーベット', 'しゃーべっと'}
    rMP = {'rmp', 'mp', 'ミュージックパーク', 'ミューパ', 'ミューぱ', 'みゅーじっくぱーく', 'みゅーぱ'}
    rYV = {'ryv', 'yv', 'ヨシバ', 'よっしーバレー', 'よっしーばれー', 'ヨッシーバレー', 'よしば', 'バレー', 'ばれー'}
    
    rTTC = {'rttc', 'ttc', 'チクタクロック', 'チクタク', 'ティックトック', 'チックタック', 'ちっくたっく', 'ちくたくろっく', 'ちくたく'}
    rPPS = {'rpps', 'pps', 'パクスラ', 'パックンスライダー', 'ぱくすら', 'ぱっくんすらいだー', 'パックン', 'ぱっくん'}
    rGV = {'rgv', 'gv', 'ぐらぐら', 'グラグラ', 'グラグラ火山', 'ぐらぐら火山', 'グラグラカザン', 'ぐらぐらかざん', '火山', 'かざん'}
    rRRd = {'rrrd', '64虹', '64にじ', '64にじ', 'ろくよん', 'ロクヨン'}

    dYC = {'dyc', 'yc', 'ヨシサ', 'ヨッシーサーキット', 'よしさ', 'よっしーさーきっと'}
    dEA = {'dea', 'ea', 'エキサイトバイク', '役馬', 'エキバ', 'えきば', 'えきさいとばいく'}
    dDD = {'ddd', 'dd', 'ドラロ', 'どらろ', 'ドラゴンロード', 'どらごんろーど'}
    dMC = {'dmc', 'ミュートシティ', 'ミュート', 'みゅーと', 'みゅーとしてぃ'}

    dWGM = {'dwgm', 'wgm', 'ワリオこうざん', 'ワリオ鉱山', 'わりおこうざん', 'わりこう', 'ワリこう', 'ワリ鉱', 'わり鉱'}
    dRR = {'drr', 'sfc', 'sfcにじ', 'sfc虹', 'えすえふしー', 'エスエフシー', 'sfcレインボーロード'}
    dIIO = {'diio', 'iio', 'ツルツルツイスター', 'つるつるついすたー', 'ツツツ', 'つつつ', 'ツイスター', 'ついすたー', 'ツルツル', 'つるつる'}
    dHC = {'dhc', 'hc', 'ハイラルサーキット', 'はいらる', 'はいらるさーきっと', 'ハイラル'}
    
    dBP = {'dbp', 'bp', 'ベビィパーク', 'ベビーパーク', 'べびーぱーく', 'べびぱ', 'ベビパ', 'ベビー'}
    dCL = {'dcl', 'cl', 'チーズランド', 'ちーずらんど', 'ちーず', 'チーズ'}
    dWW = {'dww', 'ww', 'ネイチャーロード', 'ねいちゃーろーど', 'ネイチャー', 'ねいちゃー', 'なちゅれ', 'ナチュレ'}
    dAC = {'dac', 'ac', 'どうぶつの森', 'どうもり', '動物の森', 'どう森', 'ぶつ森', 'ぶつもり', 'ドウモリ', 'ブツモリ'}

    dNBC = {'dnbc', 'nbc', 'ネオクッパシティ', 'ねおくっぱしてぃ', 'ネオぱ', 'ネオパ', 'ねおぱ', 'ねおくっぱ', 'ネオクッパ'}
    dRiR = {'drir', 'rir', 'リボンロード', 'リボン', 'りぼんろーど', 'りぼん'}
    dSBS = {'dsbs', 'sbs', 'リンリンメトロ', 'りんりんめとろ', 'りんめと', 'リンメト', 'リンリン', 'りんりん', 'リン', 'りん'}
    dBB = {'dbb', 'bb', 'ビッグブルー', 'びっぐぶるー'}

    # 追加コース第１弾
    bPP = {'bpp', 'pp', 'paris', 'ぱり', 'パリ', 'パリプロムナード', 'ぱりぷろむなーど'}
    bTC = {'btc', 'tc', 'キノピオサーキット', 'キノサ', 'きのぴおさーきっと', 'きのさ'}
    bCMo = {'bcmo', 'cmo', 'bchm', 'chm', 'bcm64', 'cm64', 'チョコマウンテン', 'チョコ', 'チョコマ', 'ちょこまうんてん', 'ちょこま', 'ちょこ', 'チョコ山', 'チョコやま'}
    bCMa = {'bcma', 'cma', 'com', 'bcom', 'bcmw', 'cmw', 'ココナッツモール', 'ココモ', 'ココナッツ', 'ここなっつもーる', 'ここも', 'ココナッツ', 'ここなっつ', 'ナッツ', 'なっつ'}

    bTB = {'btb', 'tb', 'tokyo', 'トーキョースクランブル', 'スクランブル', 'すくらんぶる', 'とーきょーすくらんぶる', 'トウキョウ', 'トーキョー', 'とうきょう', 'とーきょー', '東京'}
    bSR = {'bsr', 'sr', 'キノコリッジウェイ', 'リッジ', 'キコリ', 'きこり', 'りっじ', 'きのこりっじうぇい', 'りっじうぇい', 'リッジウェイ'}
    bSG = {'bsg', 'sg', 'gbaスカイガーデン',  'gbaすかいがーでん', 'gbaスカガ', 'gbaすかが', 'グバスカ', 'ぐばすか', 'グバガ', 'ぐばが'}
    bNH = {'bnh', 'nh', 'ninja', 'ニンニンドージョー', 'にんにんどーじょー', 'ニンニン', 'にんにん', 'にんじょー', 'ニンジョー', 'ドージョー', 'どうじょう'}

    # 追加コース第２弾
    bNYM = {'bnym', 'nym', 'ニューヨークドリーム', 'ニューヨーク', 'ニューヨーク', 'にゅーよーく', 'ニュードリ', 'にゅーどり'}
    bMC3 = {'bmc3', 'mc3', 'sfcマリサ', 'sfcまりさ', 'マリサ3', 'まりさ3'}
    bKD = {'bkd', 'kd', '64カラカラさばく', '64カラサバ', '64からさば'}
    bWP = {'bwp', 'ワルイージピンボール', 'ワルピン', 'わるぴん'}

    bSS = {'bss', 'ss', 'シドニーサンシャイン', 'シドニー', 'しどにー'}
    bSL = {'bsl', 'スノーランド', 'スノラン', 'すのらん'}
    bMG = {'bmg', 'mg', 'キノコキャニオン', 'キノキャニ', 'きのキャニ', 'きのきゃに'}
    bSHS = {'bshs', 'shs', 'アイスビルディング', 'アイス', 'あいす'}

    # 追加コース第３弾
    bLL = {'bll', 'll', 'ロンドンアベニュー', 'ロンドン', 'ろんどん'}
    bBL = {'bbl', 'bl', 'テレサレイク', 'テレレ', 'テレサ', 'レイク', 'てれされいく', 'てれれ', 'てれさ', 'れいく'}
    bRRM = {'brrm', 'rrm', 'ロックロックマウンテン', 'ロック', 'ロクマ', 'ろくま'}
    bMT = {'bmt', 'mt','メイプルツリーハウス', 'メイプル', 'メープル', 'めいぷる', 'めーぷる'}

    bBB = {'bbb', 'ベルリンシュトラーセ', 'ベルリン', 'べるりん'}
    bPG = {'bpg', 'pg', 'ピーチガーデン', 'ピチガ', 'ぴちが'}
    bMM = {'bmm', 'mm', 'メリーメリーマウンテン', 'メリマ', 'メリー', 'めりま'}
    bRR7 = {'brr7', 'brr', 'rr7', '3dsレインボーロード', '3ds虹', '3dsにじ', '7虹', '7にじ'}

    # 追加コース第４弾
    bAD = {'bad', 'ad', 'アムステルダムブルーム', 'アムステルダム', 'あむすてるだむ', 'アムス', 'あむす'}
    bRP = {'brp', 'rp', 'リバーサイドパーク', 'リバパ', 'りばぱ', 'リバサ', 'りばさ'}
    bDKS = {'bdks', 'dks', 'スノーボードクロス', 'スノボ', 'クロス', 'すのぼ', 'くろす'}
    bYI = {'byi', 'yi', 'ヨッシーアイランド', 'アイランド', 'あいらんど', 'ヨシアイ', 'よしあい'}

    bBR = {'bbr', 'br', 'バンコクラッシュ', 'バンコク', 'ばんこく'}
    bMC = {'bmc', 'dsマリオサーキット', 'dsマリサ', 'dsまりさ'}
    bWS = {'bws', 'ワルイージスタジアム', 'ワルスタ', 'わるすた'}
    bSSy = {'bssy', 'ssy', 'シンガポールスプラッシュ', 'シンガポール', 'しんがぽーる', 'シンスプ', 'しんすぷ'}

    # 追加コース第５弾
    bAtD = {'batd', 'atd', 'アテネポリス', 'アテネ', 'あてね'}
    bDC = {'bdc', 'dc', 'デイジークルーザー', 'デイクル', 'でいくる','デイジー', 'クルーザー', 'でいじー', 'くるーざー'}
    bMH = {'bmh', 'mh', 'ムーンリッジ', 'むーんりっじ', 'ムーン', 'むーん'}
    bSCS = {'bscs', 'scs', 'シャボンロード', 'シャボン', 'しゃぼん'}

    bLAL = {'blal', 'lal', 'ロサンゼルスコースト', 'ロサンゼルス', 'ろさんぜるす', 'ロス', 'ろす'}
    bSW = {'bsw', 'sw', 'サンセットこうや', 'サンセット', 'さんせっと', 'こうや'}
    bKC = {'bkc', 'kc', 'ノコノコみさき', 'のこのこみさき', 'ノコノコ', 'のこのこ', 'ノコミサ', 'ノコみさ', 'のこみさ', 'ノコみ', 'のこみ'}
    bVV = {'bvv', 'vv', 'バンクーバーバレー', 'バンクーバー', 'ばんくーばー'}

    # 追加コース第６弾
    bRA = {'bra', 'ra', 'ローマアーバンティ', 'ローマ', 'ろーま', 'アーバンティ', 'あーばんてぃ'} 
    bDKM = {'bdkm', 'dkm', 'dkマウンテン', 'dkまうんてん', 'dk山', 'dkやま'}
    bDCt = {'bdc', 'dct', 'デイジーサーキット', 'デイサ', 'でいさ'}
    bPPC = {'bppc', 'ppc', 'パックンしんでん', 'しんでん'}

    bMD = {'bmd', 'md', 'マドリード', 'まどりーど', 'マドリー', 'まどりー', 'マリグラ', 'まりぐら'}
    bRIW = {'briw', 'riw', 'ロゼッタプラネット', 'ロゼッタ', 'ろぜった', 'ロゼプラ', 'ろぜぷら', 'ロゼ', 'ろぜ'}
    bBC3 = {'bbc3', 'bc3', 'クッパ城', 'クッパじょう', 'くっぱじょう'}
    bRRw = {'brrw', 'rrw', 'wii虹', 'wiiにじ', 'wにじ', 'w虹', 'wiiレインボーロード', 'wiiれいんぼーろーど'}


    # 英語
    # tracks = [ \
    #     [['Mario Kart Stadium', MKS], ['Water Park', WP], ['Sweet Sweet Canyon', SSC], ['Thwomp Ruins', TR]], \
    #     [['Mario Circuit', MC], ['Toad Harbor', TH], ['Twisted Mansion', TM], ['Shy Guy Falls', SGF]], \
    #     [['Sunshine Airport', SA], ['Dolphin Shoals', DS], ['Electrodrome', Ed], ['Mount Wario', MW]], \
    #     [['Cloudtop Cruise', CC], ['Bone-Dry Dunes', BDD], ["Bowser's Castle", BC], ['Rainbow Road', RR]], \
    #     [['Wii Moo Moo Meadows', rMMM], ['GBA Mario Circuit', rMC], ['DS Cheep Cheep Beach', rCCB], ["N64 Toad's Turnpike", rTT]], \
    #     [['GCN Dry Dry Desert', rDDD], ['SNES Donut Plains 3', rDP3], ['N64 Royal Raceway', rRRy], ['3DS DK Jungle', rDKJ]], \
    #     [['DS Wario Stadium', rWS], ['GCN Sherbet Land', rSL], ['3DS Music Park', rMP], ['N64 Yoshi Valley', rYV]], \
    #     [['DS Tick-Tock Clock', rTTC], ['3DS Piranha Plant Slide', rPPS], ['Wii Grumble Volcano', rGV], ['N64 Rainbow Road', rRRd]], \
    #     [['GCN Yoshi Circuit', dYC], ['Excitebike Arena', dEA], ['Dragon Driftway', dDD], ['Mute City', dMC]], \
    #     [["Wii Wario's Gold Mine", dWGM], ['SNES Rainbow Road', dRR], ['Ice Ice Outpost', dIIO], ['Hyrule Circuit', dHC]], \
    #     [['GCN Baby Park', dBP], ['GBA Cheese Land', dCL], ['Wild Woods', dWW], ['Animal Crossing', dAC]], \
    #     [['3DS Neo Bowser City', dNBC], ['GBA Ribbon Road', dRiR], ['Super Bell Subway', dSBS], ['Big Blue', dBB]], \
    #     [['Tour Paris Promenade', bPP], ['3DS Toad Circuit', bTC], ['N64 Choco Mountain', bCMo], ['Wii Coconut Mall', bCMa]], \
    #     [['Tour Tokyo Blur', bTB], ['DS Shroom Ridge', bSR], ['GBA Sky Garden', bSG], ['Ninja Hideaway', bNH]], \
    #     [['Tour New York Minute', bNYM], ['SNES Mario Circuit 3', bMC3], ['N64 Kalimari Desert', bKD], ['DS Waluigi Pinball', bWP]], \
    #     [['Tour Sydney Sprint', bSS], ['GBA Snow Land', bSL], ['Wii Mushroom Gorge', bMG], ['Sky-High Sundae', bSHS]], \
    #     [['Tour London Loop', bLL], ['GBA Boo Lake', bBL], ['3DS Rock Rock Mountain', bRRM], ['Wii Maple Treeway', bMT]], \
    #     [['Tour Berlin Byways', bBB], ['DS Peach Gardens', bPG], ['Merry Mountain', bMM], ['3DS Rainbow Road', bRR7]], \
    #     [['Tour Amsterdam Drift', bAD], ['GBA Riverside Park', bRP], ['Wii DK Summit', bDKS], ['Yoshi Island', bYI]], \
    #     [['Tour Bangkok Rush', bBR], ['DS Mario Circuit', bMC], ['GCN Waluigi Stadium', bWS], ['Tour Singapore Speedway', bSSy]], \
    #     [['Tour Athens Dash', bAtD], ['GCN Daisy Cruiser', bDC], ['Wii Moonview Highway', bMH], ['Squeaky Clean Sprint', bSCS]], \
    #     [['Tour Los Angeles Laps', bLAL], ['GBA Sunset Wilds', bSW], ['Wii Koopa Cape', bKC], ['Tour Vancouver Velocity', bVV]], \
    #     [['Tour Rome Avanti', bRA], ['GCN DK Mountain', bDKM], ['Wii Daisy Circuit', bDCt], ['Piranha Plant Cove', bPPC]], \
    #     [['Tour Madrid Drive', bMD], ["3DS Rosalina's Ice World", bRIW], ['SNES Bowser Castle 3', bBC3], ['Wii Rainbow Road', bRRw]]]
    
    # 日本語
    tracks = [ \
        [['マリオカートスタジアム', MKS], ['ウォーターパーク', WP], ['スイーツキャニオン', SSC], ['ドッスンいせき', TR]], \
        [['マリオサーキット', MC], ['キノピオハーバー', TH], ['ねじれマンション', TM], ['ヘイホーこうざん', SGF]], \
        [['サンシャインくうこう', SA], ['ドルフィンみさき', DS], ['エレクトロドリーム', Ed], ['ワリオスノーマウンテン', MW]], \
        [['スカイガーデン', CC], ['ホネホネさばく', BDD], ['クッパキャッスル', BC], ['レインボーロード', RR]], \
        [['Wii モーモーカントリー', rMMM], ['GBA マリオサーキット', rMC], ['DS プクプクビーチ', rCCB], ["N64 キノピオハイウェイ", rTT]], \
        [['GC カラカラさばく', rDDD], ['SFC ドーナツへいや3', rDP3], ['N64 ピーチサーキット', rRRy], ['3DS DKジャングル', rDKJ]], \
        [['DS ワリオスタジアム', rWS], ['GC シャーベットランド', rSL], ['3DS ミュージックパーク', rMP], ['N64 ヨッシーバレー', rYV]], \
        [['DS チクタクロック', rTTC], ['3DS パックンスライダー', rPPS], ['Wii グラグラかざん', rGV], ['N64 レインボーロード', rRRd]], \
        [['GC ヨッシーサーキット', dYC], ['エキサイトバイク', dEA], ['ドラゴンロード', dDD], ['ミュートシティ', dMC]], \
        [["Wii ワリオこうざん", dWGM], ['SFC レインボーロード', dRR], ['ツルツルツイスター', dIIO], ['ハイラルサーキット', dHC]], \
        [['GC ベビィパーク', dBP], ['GBA チーズランド', dCL], ['ネイチャーロード', dWW], ['どうぶつの森', dAC]], \
        [['3DS ネオクッパシティ', dNBC], ['GBA リボンロード', dRiR], ['リンリンメトロ', dSBS], ['ビッグブルー', dBB]], \
        [['Tour パリプロムナード', bPP], ['3DS キノピオサーキット', bTC], ['N64 チョコマウンテン', bCMo], ['Wii ココナッツモール', bCMa]], \
        [['Tour トーキョースクランブル', bTB], ['DS キノコリッジウェイ', bSR], ['GBA スカイガーデン', bSG], ['ニンニンドージョー', bNH]], \
        [['Tour ニューヨークドリーム', bNYM], ['SFC マリオサーキット3', bMC3], ['N64 カラカラさばく', bKD], ['DS ワルイージピンボール', bWP]], \
        [['Tour シドニーサンシャイン', bSS], ['GBA スノーランド', bSL], ['Wii キノコキャニオン', bMG], ['アイスビルディング', bSHS]], \
        [['Tour ロンドンアベニュー', bLL], ['GBA テレサレイク', bBL], ['3DS ロックロックマウンテン', bRRM], ['Wii メイプルツリーハウス', bMT]], \
        [['Tour ベルリンシュトラーゼ', bBB], ['DS ピーチガーデン', bPG], ['メリーメリーマウンテン', bMM], ['3DS レインボーロード', bRR7]], \
        [['Tour アムステルダムブルーム', bAD], ['GBA リバーサイドパーク', bRP], ['Wii DKスノーボードクロス', bDKS], ['ヨッシーアイランド', bYI]], \
        [['Tour バンコクラッシュ', bBR], ['DS マリオサーキット', bMC], ['GC ワルイージスタジアム', bWS], ['Tour シンガポールスプラッシュ', bSSy]], \
        [['Tour アテネポリス', bAtD], ['GC デイジークルーザー', bDC], ['Wii ムーンリッジ&ハイウェイ', bMH], ['シャボンロード', bSCS]], \
        [['Tour ロサンゼルスコースト', bLAL], ['GBA サンセットこうや', bSW], ['Wii ノコノコみさき', bKC], ['Tour バンクーバーバレー', bVV]], \
        [['Tour ローマアバンティ', bRA], ['GC DKマウンテン', bDKM], ['Wii デイジーサーキット', bDCt], ['パックンしんでん', bPPC]], \
        [['Tour マドリードグランデ', bMD], ["3DS ロゼッタプラネット", bRIW], ['SFC クッパじょう3', bBC3], ['Wii レインボーロード', bRRw]]]

    
    
    for i in range(24):
        for j in range(4):
            if name in tracks[i][j][1]:
                n = i*4 + j

                # コース名, 番号(0~95)を返す 
                return [tracks[i][j][0], n+OFFSET]
    
    return None