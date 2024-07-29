# nameに対応するランクIDを返す
def search(name) -> str:
    name = str.lower(name)

    IRON = ['iron', 'アイアン', 'あいあん', '鉄', 'てつ']
    BRONZE = ['bronze', 'ブロンズ', 'ぶろんず', '銅', 'どう']
    SILVER = ['silver', 'シルバー', 'しるばー', '銀', 'ぎん']
    GOLD = ['gold', 'ゴールド', 'ごーるど', '金', 'きん']
    PLATINUM = ['platinum', 'plat', 'プラチナ', 'ぷらちな', 'プラット', 'ぷらっと', '白金', 'はっきん', '水', 'みず']
    SAPPHIRE = ['sapphire', 'サファイア', 'さふぁいあ', 'サファ', 'さふぁ', '青', 'あお']
    RUBY = ['ruby', 'ルビー', 'るびー', '赤', 'あか']

    # DIAMOND = ['diamond', 'ダイヤモンド', 'だいやもんど', 'ダイヤ', 'だいや']
    # MASTER = ['master', 'マスター']
    # GRANDMASTER = ['grandmaster', 'グランドマスター', 'ぐらんどますたー', 'グラマス', 'ぐらます']


    ranks = [IRON, BRONZE, SILVER, GOLD, PLATINUM, SAPPHIRE, RUBY]
    for i, rank in enumerate(ranks):
        if name in rank:
            return i
    
    return -1


def rank_name(rank_id) -> str:
    ranks = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Sapphire', 'Ruby', 'Diamond', 'Master', 'Grandmaster']
    return ranks[rank_id]


def rank_color(rank_id) -> int:
    colors = [0x817876, 0xE67E22, 0x7D8396, 0xF1C40F, 0x3FABB8, 0x286CD3, 0xD51C5E, 0x9CCBD6, 0x0E0B0B, 0xA3022C]

    return colors[rank_id]