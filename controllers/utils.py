import pandas as pd

# タイムを秒に変換: 120000 -> 80sec
def convert_time_into_seconds(time: str) -> float:
    minutes, seconds, milliseconds = map(int, (time[0], time[1:3], time[3:]))
    return minutes * 60 + seconds + milliseconds / 1000


# 秒をタイムに変換: 120.000 -> 200000
def convert_seconds_into_time(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds - m*60)
    decimal = '{:.3f}'.format(seconds - int(seconds))[2:]
    return f'{m}{str(s).zfill(2)}{decimal}'


# タイム差を計算
def calc_time_diff(time1: str, time2: str) -> str:
	t1_sec = convert_time_into_seconds(time1)
	t2_sec = convert_time_into_seconds(time2)
	return '{:.3f}'.format(t1_sec - t2_sec)


# タイムのフォーマット: 120000 -> 1:20.000
def format_time(time: str) -> str:
	return time[0] + ':' + time[1] + time[2] + '.' + time[3:]


# タイムのフォーマットを解除: 1:20.000 -> 120000
def unformat_time(time: str) -> str:
    return time.replace(':', '').replace('.', '')

# タイム差のフォーマット
def format_diff(diff: str) -> str:
    if diff[0] == '-':
        return diff
    return '+' + diff

# サムネイルのURLを取得
def get_thumbnail_url(row: int) -> str:
	return f'https://raw.githubusercontent.com/Takuma515/discord-bot/main/images/{row-4}.png'


# 全角数字を半角数字に変換
def convert_full_to_half(num: str) -> str:
    zenkaku_table = str.maketrans({
    '１': '1',
    '２': '2',
    '３': '3',
    '４': '4',
    '５': '5',
    '６': '6',
    '７': '7',
    '８': '8',
    '９': '9',
    '０': '0',
    })

    return num.translate(zenkaku_table)