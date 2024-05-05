import discord
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# スプレッドシートの設定とアクセス
file_name = 'NITA'
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
key = os.environ['API_KEY']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(key), scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)
wks = sh.worksheet('UserData')

# 行番号の設定
USER_ROW = 1
ID_ROW = 2
MMR_ROW = 3


# 列番号の設定
TRACK_COL = 1
WR_PLAYER_COL = 2
WR_TIME_COL = 4
WR_LINK_COL = 5
VIDEO_COL = 6

# 定数
EMBED_LIMIT = 25


# userをIDで検索し列番号を返す
def search_user(author: discord.member.Member) -> int:
	id_list = wks.row_values(ID_ROW)
	col = len(id_list) + 1
	id = str(author.id)

	if id in id_list:
		col = id_list.index(id) + 1
	else:
		# userが見つからなかった場合
		# wks.add_cols(1)
		wks.update_cell(ID_ROW, col, id)
		
	# ユーザ名の更新
	wks.update_cell(USER_ROW, col, author.name)

	return col


# ユーザの記録を取得
def fetch_user_record(track_id: int, col_id: int) -> str:
	return wks.cell(track_id, col_id).value


# ユーザの全ての記録を取得
def fetch_all_user_records(col_id: int) -> list:
	return wks.col_values(col_id)


# ユーザの記録を更新
def update_record(track_id: int, col_id: int, time: str) -> None:
	wks.update_cell(track_id, col_id, time)


# ユーザの記録を削除
def delete_record(track_id: int, author: discord.member.Member) -> None:
	col_id = search_user(author)
	wks.update_cell(track_id, col_id, '')


# 全てのユーザの名前とIDを取得
def fetch_user_list() -> list:
	user_names = wks.row_values(USER_ROW)
	user_ids = wks.row_values(ID_ROW)
	return [user_names, user_ids]


# ユーザのMMRを取得
def fetch_mmr_list() -> list:
	mmr_list = wks.row_values(MMR_ROW)
	return mmr_list


# 指定コースの全ての記録を取得
def fetch_track_records(track_id: int) -> list:
	return wks.row_values(track_id)


# コース名一覧を取得
def fetch_track_name() -> list:
	return wks.col_values(TRACK_COL)


# WRのプレイヤー名、タイム、リンクを取得
def fetch_wr_info(track_id: int) -> list:
	wr_player = wks.cell(track_id, WR_PLAYER_COL).value
	wr_time = wks.cell(track_id, WR_TIME_COL).value
	wr_link = wks.cell(track_id, WR_LINK_COL).value
	return [wr_player, wr_time, wr_link]


# 全てのコースのWRのプレイヤー名、タイム、リンクを取得
def fetch_all_wr_info() -> list:
	wr_players = wks.col_values(WR_PLAYER_COL)
	wr_times = wks.col_values(WR_TIME_COL)
	wr_links = wks.col_values(WR_LINK_COL)
	return [wr_players, wr_times, wr_links]


# WR (1〜15位) のタイム、プレイヤー名、リンクを取得
def fetch_wr_list(track_id: int) -> list:
	wks = sh.worksheet('WR List')
	track_id = track_id - 4

	start = track_id*21 + 20
	end = start + 14

	# データの取得
	players = wks.range(f'L{start}:L{end}')
	times = wks.range(f'M{start}:M{end}')

	# データの整形
	players = [player.value for player in players]
	times = [time.value[0:8] for time in times]

	return [players, times]


# 解説動画のリンクを取得
def fetch_video_url(track_id: int) -> str:
	return wks.cell(track_id, VIDEO_COL).value
