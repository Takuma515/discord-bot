def search(name):
    name = str.lower(name)
    MKS_list = {'MKS', 'mks', 'マリオカートスタジアム', 'まりおかーとすたじあむ', 'マリカス', 'まりかす'}
    WP_list = {'WP', 'wp', 'ウォーターパーク','うぉーたーぱーく','うぉたぱ', 'ウォタパ'}
    SSC_list = {'SSC', 'ssc', 'スイーツキャニオン', 'すいーつきゃにおん', 'スイキャニ', 'すいきゃに'}
    TR_list = {'TR', 'tr', 'ドッスン遺跡', 'どっすんいせき', 'ドッスンいせき', 'ドッスンイセキ', 'ドッスン', 'どっすん', 'いせき', '遺跡', 'イセキ'}

    MC_list = {'MC', 'mc', 'マリオサーキット', 'マリサ', 'まりおさーきっと', 'まりさ', '新マリサ', 'しんまりさ', 'シンマリサ', '新まりさ'}
    TH_list = {'TH', 'th', 'キノピオハーバー', 'きのぴおはーばー', 'はーばー', 'ハーバー'}
    TM_list = {'TM', 'tm', 'ねじれマンション', 'ねじれまんしょん', 'ねじまん', 'ねじマン', 'ネジマン', 'まんしょん', 'マンション', 'ねじれ', 'ネジレ', 'ねじ', 'ネジ'}
    SGF_list = {'SGF', 'sgf', 'へいほーこうざん', 'ヘイホー鉱山', 'ヘイホーこうざん', 'へいほー鉱山', 'へいこう', 'ヘイコウ', 'へい鉱', 'ヘイ鉱', 'ヘイこう'}

    SA_list = {'SA', 'sa', 'サンシャイン空港', 'サンシャインくうこう', 'さんしゃいんくうこう', '空港', 'くうこう'}
    DS_list = {'DS', 'ds', 'ドルフィンみさき', 'ドルフィン岬', 'どるふぃんみさき', 'どるふぃん岬', 'どるみ', 'ドルミ', 'どるふぃん', 'ドルフィン'}
    Ed_list = {'Ed', 'ed', 'ED', 'エレドリ', 'エレド', 'エレクトロドリーム', 'えれどり', 'えれど', 'えれくとろどりーむ'}
    MW_list = {'MW', 'mw', 'ワリオスノーマウンテン', 'わりおすのーまうんてん', 'ワリスノ', 'わりすの', '雪山', 'ゆきやまうんてん', 'すの', 'スノ'}

    CC_list = {'CC', 'cc', 'スカイガーデン', 'スカが', 'すかが', 'スカガ', 'すかいがーでん'}
    BDD_list = {'BDD', 'bdd', 'ホネホネさばく', 'ホネホネ砂漠', 'ほねほねさばく', 'ほねほね砂漠', '骨骨砂漠', '骨骨さばく', 'ホネホネサバク', 'ほねさば', '骨サバ', 'ホネサバ', '骨', 'ほね', 'ホネ', 'ほねほね', '骨骨', 'ホネホネ'}
    BC_list = {'BC', 'bc', 'クッパキャッスル', 'くっぱきゃっする', 'くっきゃぱっする', 'クッキャパッスル', 'くぱきゃ', 'クパキャ'}
    RR_list = {'RR', 'rr', '新虹', 'しんにじ', 'レインボーロード', 'シンニジ', 'れいんぼーろーど'}

    MMM_list = {'rMMM', 'rmmm', 'mmm', 'モモカン', 'もーもーカントリー', 'モーモーカントリー', 'ももかん', 'もーもーかんとりー', '牛', 'うし'}
    rMC_list = {'rMC', 'rmc', 'RMC', 'GBA', 'ぐば', 'グバ', 'GBAまりさ', 'GBAマリサ', 'GBAマリオサーキット', 'GBAまりおさーきっと', 'ジービーエー', 'じーびーえー'}
    CCB_list = {'rCCB', 'rccb', 'ccb', 'プクプクビーチ', 'プクプク', 'プクビ', 'ぷくぷくびーち', 'ぷくぷく', 'ぷくび', 'びーち', 'ビーチ'}
    TT_list = {'rTT', 'rtt', 'tt', 'キノピオハイウェイ', '高速道路', '高速', 'こうそくどうろ', 'こうそく', 'はいうぇい', 'ハイウェイ', 'きのぴおはいうぇい'}

    DDD_list = {'rDDD', 'rddd', 'RDDD', 'カラカラ', 'カラサバ', 'からさば', 'からから', 'カラカラ砂漠', 'からからさばく', 'カラカラさばく', 'カラカラサバク'}
    DP3_list = {'rDP3', 'rdp3', 'dp3', 'ドーナツへいや', 'どーなつへいや', 'ドーナツ平野', 'どーなつ平野', 'ドーナツヘイヤ', '平野', 'へいや'}
    rRRy_list = {'rRRy', 'rrry', 'RRRY', 'ピーチサーキット', 'ぴーちさーきっと', 'ピチさ', 'ピチサ', 'ぴちさ'}
    DKJ_list = {'rDKJ', 'rdkj', 'dkj', 'じゃんぐる', 'ジャングル', 'dk'}

    WS_list = {'rWS', 'rws', 'ws', 'ワリオスタジアム', 'ワリスタ', 'わりすた', 'わりおすたじあむ'}
    SL_list = {'rSL', 'rsl', 'sl', 'しゃべらん', 'シャベラン', 'シャーベットランド', 'しゃーべっとらんど', 'シャーベット', 'しゃーべっと'}
    MP_list = {'rMP', 'rmp', 'mp', 'ミュージックパーク', 'ミューパ', 'ミューぱ', 'みゅーじっくぱーく', 'みゅーぱ'}
    YV_list = {'rYV', 'ryv', 'yv', 'ヨシバ', 'よっしーバレー', 'よっしーばれー', 'ヨッシーバレー', 'よしば', 'バレー', 'ばれー'}
    
    TTC_list = {'rTTC', 'rttc', 'ttc', 'チクタクロック', 'チクタク', 'ティックトック', 'チックタック', 'ちっくたっく', 'ちくたくろっく', 'ちくたく'}
    PPS_list = {'rPPS', 'rpps', 'pps', 'パクスラ', 'パックンスライダー', 'ぱくすら', 'ぱっくんすらいだー', 'パックン', 'ぱっくん'}
    GV_list = {'rGV', 'rgv', 'gv', 'ぐらぐら', 'グラグラ', 'グラグラ火山', 'ぐらぐら火山', 'グラグラカザン', 'ぐらぐらかざん', '火山', 'かざん'}
    rRRd_list = {'rRRd', 'rrrd', 'RRRD', '64虹', '６４虹', '64にじ', '６４にじ', 'ろくよん', 'ロクヨン'}

    dYC_list = {'dYC', 'dyc', 'DYC', 'ヨシサ', 'ヨッシーサーキット', 'よしさ', 'よっしーさーきっと'}
    dEA_list = {'dEA', 'dea', 'DEA', 'エキサイトバイク', '役馬', 'エキバ', 'えきば', 'えきさいとばいく'}
    dDD_list = {'dDD', 'ddd', 'DDD', 'ドラロ', 'どらろ', 'ドラゴンロード', 'どらごんろーど'}
    dMC_list = {'dMC', 'dmc', 'DMC', 'ミュートシティ', 'ミュート', 'みゅーと', 'みゅーとしてぃ'}

    dWGM_list = {'dWGM', 'dwgm', 'DWGM', 'ワリオこうざん', 'ワリオ鉱山', 'わりおこうざん', 'わりこう', 'ワリこう', 'ワリ鉱', 'わり鉱'}
    dRR_list = {'dRR', 'drr', 'DRR', 'SFC', 'sfc', 'SFCにじ', 'SFC虹', 'sfcにじ', 'sfc虹', 'えすえふしー', 'エスエフシー', 'SFCレインボーロード', 'sfcレインボーロード'}
    dIIO_list = {'dIIO', 'diio', 'DIIO', 'ツルツルツイスター', 'つるつるついすたー', 'ツツツ', 'つつつ', 'ツイスター', 'ついすたー', 'ツルツル', 'つるつる'}
    dHC_list = {'dHC', 'dhc', 'DHC', 'ハイラルサーキット', 'はいらる', 'はいらるさーきっと', 'ハイラル'}
    
    dBP_list = {'dBP', 'dbp', 'DBP', 'BP', 'bp', 'ベビィパーク', 'ベビーパーク', 'べびぃぱーく', 'べびーぱーく', 'べびぱ', 'ベビパ'}
    dCL_list = {'dCL', 'dcl', 'DCL', 'チーズランド', 'ちーずらんど', 'ちーず', 'チーズ'}
    dWW_list = {'dWW', 'dww', 'DWW', 'ネイチャーロード', 'ねいちゃーろーど', 'ネイチャー', 'ねいちゃー', 'なちゅれ', 'ナチュレ'}
    dAC_list = {'dAC', 'dac', 'DAC', 'ac', 'AC', 'どうぶつの森', 'どうもり', '動物の森', 'どう森', 'ぶつ森', 'ぶつもり', 'ドウモリ', 'ブツモリ'}

    dNBC_list = {'dNBC', 'dnbc', 'DNBC', 'ネオクッパシティ', 'ねおくっぱしてぃ', 'ネオぱ', 'ネオパ', 'ねおぱ', 'ねおくっぱ', 'ネオクッパ'}
    dRiR_list = {'dRiR', 'DRIR', 'drir', 'リボンロード', 'リボン', 'りぼんろーど', 'りぼん'}
    dSBS_list = {'dSBS', 'dsbs', 'DSBS', 'リンリンメトロ', 'りんりんめとろ', 'りんめと', 'リンメト', 'リンリン', 'りんりん', 'リン', 'りん'}
    dBB_list = {'dBB', 'dbb', 'bb', 'ビッグブルー', 'びっぐぶるー'}

    # 新コース
    bPP_list = {'bPP', 'bpp', 'pp', 'paris', 'ぱり', 'パリ', 'パリプロムナード', 'ぱりぷろむなーど'}
    bTC_list = {'bTC', 'btc', 'tc', 'キノピオサーキット', 'キノサ', 'きのぴおさーきっと', 'きのさ'}
    bCMo_list = {'bCMo', 'bcmo', 'cmo', 'bchm', 'chm', 'bcm64', 'cm64', 'チョコマウンテン', 'チョコ', 'チョコマ', 'ちょこまうんてん', 'ちょこま', 'ちょこ', 'チョコ山'}
    bCMa_list = {'bCMa', 'bcma', 'cma', 'com', 'bcom', 'bcmw', 'cmw', 'ココナッツモール', 'ココモ', 'ココナッツ', 'ここなっつもーる', 'ここも', 'ココナッツ', 'ここなっつ', 'ナッツ', 'なっつ'}

    bTB_list = {'bTB', 'btb', 'tb', 'tokyo', 'トーキョースクランブル', 'スクランブル', 'すくらんぶる', 'とーきょーすくらんぶる', 'トウキョウ', 'トーキョー', 'とうきょう', 'とーきょー', '東京'}
    bSR_list = {'bSR', 'bsr', 'sr', 'キノコリッジウェイ', 'リッジ', 'キコリ', 'きこり', 'りっじ', 'きのこりっじうぇい', 'りっじうぇい', 'リッジウェイ'}
    bSG_list = {'bSG', 'bsg', 'sg', 'gbaスカイガーデン',  'gbaすかいがーでん', 'gbaスカガ', 'gbaすかが', 'グバスカ', 'ぐばすか', 'グバガ', 'ぐばが'}
    bNH_list = {'bNH', 'bnh', 'nh', 'ninja', 'ニンニンドージョー', 'にんにんどーじょー', 'ニンニン', 'にんにん', 'にんじょー', 'ニンジョー', 'ドージョー', 'どうじょう'}

    
    tracks_list = [ \
        [['Mario Kart Stadium', MKS_list], ['Water Park', WP_list], ['Sweet Sweet Canyon', SSC_list], ['Thwomp Ruins', TR_list]], \
        [['Mario Circuit', MC_list], ['Toad Harbor', TH_list], ['Twisted Mansion', TM_list], ['Shy Guy Falls', SGF_list]], \
        [['Sunshine Airport', SA_list], ['Dolphin Shoals', DS_list], ['Electrodrome', Ed_list], ['Mount Wario', MW_list]], \
        [['Cloudtop Cruise', CC_list], ['Bone-Dry Dunes', BDD_list], ["Bowser's Castle", BC_list], ['Rainbow Road', RR_list]], \
        [['Wii Moo Moo Meadows', MMM_list], ['GBA Mario Circuit', rMC_list], ['DS Cheep Cheep Beach', CCB_list], ["N64 Toad's Turnpike", TT_list]], \
        [['GCN Dry Dry Desert', DDD_list], ['SNES Donut Plains 3', DP3_list], ['N64 Royal Raceway', rRRy_list], ['3DS DK Jungle', DKJ_list]], \
        [['DS Wario Stadium', WS_list], ['GCN Sherbet Land', SL_list], ['3DS Music Park', MP_list], ['N64 Yoshi Valley', YV_list]], \
        [['DS Tick-Tock Clock', TTC_list], ['3DS Piranha Plant Slide', PPS_list], ['Wii Grumble Volcano', GV_list], ['N64 Rainbow Road', rRRd_list]], \
        [['GCN Yoshi Circuit', dYC_list], ['Excitebike Arena', dEA_list], ['Dragon Driftway', dDD_list], ['Mute City', dMC_list]], \
        [["Wii Wario's Gold Mine", dWGM_list], ['SNES Rainbow Road', dRR_list], ['Ice Ice Outpost', dIIO_list], ['Hyrule Circuit', dHC_list]], \
        [['GCN Baby Park', dBP_list], ['GBA Cheese Land', dCL_list], ['Wild Woods', dWW_list], ['Animal Crossing', dAC_list]], \
        [['3DS Neo Bowser City', dNBC_list], ['GBA Ribbon Road', dRiR_list], ['Super Bell Subway', dSBS_list], ['Big Blue', dBB_list]], \
        [['Tour Paris Promenade', bPP_list], ['3DS Toad Circuit', bTC_list], ['N64 Choco Mountain', bCMo_list], ['Wii Coconut Mall', bCMa_list]], \
        [['Tour Tokyo Blur', bTB_list], ['DS Shroom Ridge', bSR_list], ['GBA Sky Garden', bSG_list], ['Tour Ninja Hideaway', bNH_list]]]
    
    for i in range(14):
        for j in range(4):
            if name in tracks_list[i][j][1]:
                n = i*4 + j
                return [tracks_list[i][j][0], n]
    
    return None