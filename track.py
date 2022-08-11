def search(name):
    name = str.lower(name)
    MKS_list = {'mks', 'マリオカートスタジアム', 'まりおかーとすたじあむ', 'マリカス', 'まりかす'}
    WP_list = {'wp', 'ウォーターパーク','うぉーたーぱーく','うぉたぱ', 'ウォタパ'}
    SSC_list = {'ssc', 'スイーツキャニオン', 'すいーつきゃにおん', 'スイキャニ', 'すいきゃに'}
    TR_list = {'tr', 'ドッスン遺跡', 'どっすんいせき', 'ドッスンいせき', 'ドッスンイセキ', 'ドッスン', 'どっすん', 'いせき', '遺跡', 'イセキ'}

    MC_list = {'mc', 'マリオサーキット', 'マリサ', 'まりおさーきっと', 'まりさ', '新マリサ', 'しんまりさ', 'シンマリサ', '新まりさ'}
    TH_list = {'th', 'キノピオハーバー', 'きのぴおはーばー', 'はーばー', 'ハーバー'}
    TM_list = {'tm', 'ねじれマンション', 'ねじれまんしょん', 'ねじまん', 'ねじマン', 'ネジマン', 'まんしょん', 'マンション', 'ねじれ', 'ネジレ', 'ねじ', 'ネジ'}
    SGF_list = {'sgf', 'へいほーこうざん', 'ヘイホー鉱山', 'ヘイホーこうざん', 'へいほー鉱山', 'へいこう', 'ヘイコウ', 'へい鉱', 'ヘイ鉱', 'ヘイこう'}

    SA_list = {'sa', 'サンシャイン空港', 'サンシャインくうこう', 'さんしゃいんくうこう', '空港', 'くうこう'}
    DS_list = {'ds', 'ドルフィンみさき', 'ドルフィン岬', 'どるふぃんみさき', 'どるふぃん岬', 'どるみ', 'ドルミ', 'どるふぃん', 'ドルフィン'}
    Ed_list = {'ed', 'エレドリ', 'エレド', 'エレクトロドリーム', 'えれどり', 'えれど', 'えれくとろどりーむ'}
    MW_list = {'mw', 'ワリオスノーマウンテン', 'わりおすのーまうんてん', 'ワリスノ', 'わりすの', '雪山', 'ゆきやまうんてん', 'すの', 'スノ'}

    CC_list = {'cc', 'スカイガーデン', 'スカガ', 'スカが', 'すかが',  'すかいがーでん'}
    BDD_list = {'bdd', 'ホネホネさばく', 'ホネホネ砂漠', 'ほねほねさばく', 'ほねほね砂漠', '骨骨砂漠', '骨骨さばく', 'ホネホネサバク', 'ほねさば', '骨サバ', 'ホネサバ', '骨', 'ほね', 'ホネ', 'ほねほね', '骨骨', 'ホネホネ'}
    BC_list = {'bc', 'クッパキャッスル', 'くっぱきゃっする', 'くっきゃぱっする', 'クッキャパッスル', 'くぱきゃ', 'クパキャ'}
    RR_list = {'rr', '新虹', '新にじ', 'しんにじ', 'レインボーロード', 'シンニジ', 'れいんぼーろーど'}

    rMMM_list = {'rmmm', 'mmm', 'モモカン', 'もーもーカントリー', 'モーモーカントリー', 'ももかん', 'もーもーかんとりー', '牛', 'うし'}
    rMC_list = {'rmc', 'gba', 'ぐば', 'グバ', 'gbaまりさ', 'gbaマリサ', 'gbaマリオサーキット', 'gbaまりおさーきっと', 'ジービーエー', 'じーびーえー'}
    rCCB_list = {'rccb', 'ccb', 'プクプクビーチ', 'プクプク', 'プクビ', 'ぷくぷくびーち', 'ぷくぷく', 'ぷくび', 'びーち', 'ビーチ'}
    rTT_list = {'rtt', 'tt', 'キノピオハイウェイ', '高速道路', '高速', 'こうそくどうろ', 'こうそく', 'はいうぇい', 'ハイウェイ', 'きのぴおはいうぇい'}

    rDDD_list = {'rddd', 'カラカラ', 'カラサバ', 'からさば', 'からから', 'カラカラ砂漠', 'からからさばく', 'カラカラさばく', 'カラカラサバク'}
    rDP3_list = {'rdp3', 'dp3', 'ドーナツへいや', 'どーなつへいや', 'ドーナツ平野', 'どーなつ平野', 'ドーナツヘイヤ', '平野', 'へいや'}
    rRRy_list = {'rrry', 'ピーチサーキット', 'ぴーちさーきっと', 'ピチさ', 'ピチサ', 'ぴちさ'}
    rDKJ_list = {'rdkj', 'dkj', 'dk', 'じゃんぐる', 'ジャングル'}

    rWS_list = {'rws', 'ws', 'ワリオスタジアム', 'ワリスタ', 'わりすた', 'わりおすたじあむ'}
    rSL_list = {'rsl', 'sl', 'しゃべらん', 'シャベラン', 'シャーベットランド', 'しゃーべっとらんど', 'シャーベット', 'しゃーべっと'}
    rMP_list = {'rmp', 'mp', 'ミュージックパーク', 'ミューパ', 'ミューぱ', 'みゅーじっくぱーく', 'みゅーぱ'}
    rYV_list = {'ryv', 'yv', 'ヨシバ', 'よっしーバレー', 'よっしーばれー', 'ヨッシーバレー', 'よしば', 'バレー', 'ばれー'}
    
    rTTC_list = {'rttc', 'ttc', 'チクタクロック', 'チクタク', 'ティックトック', 'チックタック', 'ちっくたっく', 'ちくたくろっく', 'ちくたく'}
    rPPS_list = {'rpps', 'pps', 'パクスラ', 'パックンスライダー', 'ぱくすら', 'ぱっくんすらいだー', 'パックン', 'ぱっくん'}
    rGV_list = {'rgv', 'gv', 'ぐらぐら', 'グラグラ', 'グラグラ火山', 'ぐらぐら火山', 'グラグラカザン', 'ぐらぐらかざん', '火山', 'かざん'}
    rRRd_list = {'rrrd', '64虹', '６４虹', '64にじ', '６４にじ', 'ろくよん', 'ロクヨン'}

    dYC_list = {'dyc', 'yc', 'ヨシサ', 'ヨッシーサーキット', 'よしさ', 'よっしーさーきっと'}
    dEA_list = {'dea', 'ea', 'エキサイトバイク', '役馬', 'エキバ', 'えきば', 'えきさいとばいく'}
    dDD_list = {'ddd', 'dd', 'ドラロ', 'どらろ', 'ドラゴンロード', 'どらごんろーど'}
    dMC_list = {'dmc', 'ミュートシティ', 'ミュート', 'みゅーと', 'みゅーとしてぃ'}

    dWGM_list = {'dwgm', 'wgm', 'ワリオこうざん', 'ワリオ鉱山', 'わりおこうざん', 'わりこう', 'ワリこう', 'ワリ鉱', 'わり鉱'}
    dRR_list = {'drr', 'sfc', 'sfcにじ', 'sfc虹', 'えすえふしー', 'エスエフシー', 'sfcレインボーロード'}
    dIIO_list = {'diio', 'iio', 'ツルツルツイスター', 'つるつるついすたー', 'ツツツ', 'つつつ', 'ツイスター', 'ついすたー', 'ツルツル', 'つるつる'}
    dHC_list = {'dhc', 'hc', 'ハイラルサーキット', 'はいらる', 'はいらるさーきっと', 'ハイラル'}
    
    dBP_list = {'dbp', 'bp', 'ベビィパーク', 'ベビーパーク', 'べびぃぱーく', 'べびーぱーく', 'べびぱ', 'ベビパ'}
    dCL_list = {'dcl', 'cl', 'チーズランド', 'ちーずらんど', 'ちーず', 'チーズ'}
    dWW_list = {'dww', 'ww', 'ネイチャーロード', 'ねいちゃーろーど', 'ネイチャー', 'ねいちゃー', 'なちゅれ', 'ナチュレ'}
    dAC_list = {'dac', 'ac', 'どうぶつの森', 'どうもり', '動物の森', 'どう森', 'ぶつ森', 'ぶつもり', 'ドウモリ', 'ブツモリ'}

    dNBC_list = {'dnbc', 'nbc', 'ネオクッパシティ', 'ねおくっぱしてぃ', 'ネオぱ', 'ネオパ', 'ねおぱ', 'ねおくっぱ', 'ネオクッパ'}
    dRiR_list = {'drir', 'rir', 'リボンロード', 'リボン', 'りぼんろーど', 'りぼん'}
    dSBS_list = {'dsbs', 'sbs', 'リンリンメトロ', 'りんりんめとろ', 'りんめと', 'リンメト', 'リンリン', 'りんりん', 'リン', 'りん'}
    dBB_list = {'dbb', 'bb', 'ビッグブルー', 'びっぐぶるー'}

    # 新コース
    bPP_list = {'bpp', 'pp', 'paris', 'ぱり', 'パリ', 'パリプロムナード', 'ぱりぷろむなーど'}
    bTC_list = {'btc', 'tc', 'キノピオサーキット', 'キノサ', 'きのぴおさーきっと', 'きのさ'}
    bCMo_list = {'bcmo', 'cmo', 'bchm', 'chm', 'bcm64', 'cm64', 'チョコマウンテン', 'チョコ', 'チョコマ', 'ちょこまうんてん', 'ちょこま', 'ちょこ', 'チョコ山', 'チョコやま'}
    bCMa_list = {'bcma', 'cma', 'com', 'bcom', 'bcmw', 'cmw', 'ココナッツモール', 'ココモ', 'ココナッツ', 'ここなっつもーる', 'ここも', 'ココナッツ', 'ここなっつ', 'ナッツ', 'なっつ'}

    bTB_list = {'btb', 'tb', 'tokyo', 'トーキョースクランブル', 'スクランブル', 'すくらんぶる', 'とーきょーすくらんぶる', 'トウキョウ', 'トーキョー', 'とうきょう', 'とーきょー', '東京'}
    bSR_list = {'bsr', 'sr', 'キノコリッジウェイ', 'リッジ', 'キコリ', 'きこり', 'りっじ', 'きのこりっじうぇい', 'りっじうぇい', 'リッジウェイ'}
    bSG_list = {'bsg', 'sg', 'gbaスカイガーデン',  'gbaすかいがーでん', 'gbaスカガ', 'gbaすかが', 'グバスカ', 'ぐばすか', 'グバガ', 'ぐばが'}
    bNH_list = {'bnh', 'nh', 'ninja', 'ニンニンドージョー', 'にんにんどーじょー', 'ニンニン', 'にんにん', 'にんじょー', 'ニンジョー', 'ドージョー', 'どうじょう'}

    
    tracks_list = [ \
        [['Mario Kart Stadium', MKS_list], ['Water Park', WP_list], ['Sweet Sweet Canyon', SSC_list], ['Thwomp Ruins', TR_list]], \
        [['Mario Circuit', MC_list], ['Toad Harbor', TH_list], ['Twisted Mansion', TM_list], ['Shy Guy Falls', SGF_list]], \
        [['Sunshine Airport', SA_list], ['Dolphin Shoals', DS_list], ['Electrodrome', Ed_list], ['Mount Wario', MW_list]], \
        [['Cloudtop Cruise', CC_list], ['Bone-Dry Dunes', BDD_list], ["Bowser's Castle", BC_list], ['Rainbow Road', RR_list]], \
        [['Wii Moo Moo Meadows', rMMM_list], ['GBA Mario Circuit', rMC_list], ['DS Cheep Cheep Beach', rCCB_list], ["N64 Toad's Turnpike", rTT_list]], \
        [['GCN Dry Dry Desert', rDDD_list], ['SNES Donut Plains 3', rDP3_list], ['N64 Royal Raceway', rRRy_list], ['3DS DK Jungle', rDKJ_list]], \
        [['DS Wario Stadium', rWS_list], ['GCN Sherbet Land', rSL_list], ['3DS Music Park', rMP_list], ['N64 Yoshi Valley', rYV_list]], \
        [['DS Tick-Tock Clock', rTTC_list], ['3DS Piranha Plant Slide', rPPS_list], ['Wii Grumble Volcano', rGV_list], ['N64 Rainbow Road', rRRd_list]], \
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