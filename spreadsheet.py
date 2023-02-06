import discord
import os
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import matplotlib.pyplot as plt
from io import BytesIO

# スプレッドシートの設定とアクセス
file_name = 'NITA'
scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']
key = os.environ['API_KEY']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(key), scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)

# 色の設定
green = 0x00ff00
light_blue = 0x00ffff

USER_ROW = 1
ID_ROW = 2
TRACK_COL = 1
PLAYER_COL = 2
WR_COL = 4
VIDEO_COL = 5

# userをIDで探して列番号を返す
def search_user(author: discord.member.Member, server: str) -> int:
	wks = sh.worksheet(server)
	id_list = wks.row_values(ID_ROW)
	col = len(id_list) + 1
	id = str(author.id)
	user_name = str(author)

	if id in id_list:
		col = id_list.index(id) + 1
	else:
		# userが見つからなかったので登録する
		wks.update_cell(ID_ROW, col, id)
		
	# ユーザ名の更新
	wks.update_cell(USER_ROW, col, user_name)

	return col


# タイムを秒に変換
def convert_time_into_seconds(time: str) -> float:
	return float(time[0])*60 + float(time[1])*10 + float(time[2]) + float(time[3:]) / 1000


# タイム差を計算
def calc_time_diff(time1: str, time2: str) -> str:
	t1_sec = convert_time_into_seconds(time1)
	t2_sec = convert_time_into_seconds(time2)
	return '{:.3f}'.format(t1_sec - t2_sec)


# タイムのフォーマット
def format_time(time: str) -> str:
	return time[0] + ':' + time[1] + time[2] + '.' + time[3:]


# サムネイルのURLを取得
def get_thumbnail_url(row: int) -> str:
	if row < 51:
		# 旧コース
		track_id1 = (row-3) // 4 + 1
		track_id2 = (row-2) - (track_id1-1) * 4
		return f'https://www.nintendo.co.jp/switch/aabpa/assets/images/course/thumbnail/{track_id1}-{track_id2}.jpg'
	else:
		# 新コース
		vol = (row - 51) // 8 + 1
		cup = ((row - 3) % 8) // 4 + 1
		cover = (row - 3) % 4 + 1
		return f'https://www.nintendo.co.jp/switch/aabpa/assets/images/coursepack/lineup/vol0{vol}/vol0{vol}_cup0{cup}_cover0{cover}.jpg'


def set_record(
    author: discord.member.Member,
    time: str,
    server: str,
    track: str,
    row: int) -> discord.Embed:
	wks = sh.worksheet(server)
	col = search_user(author, server)
	wr_time = sh.worksheet('WR List').cell(row, WR_COL).value
	diff = calc_time_diff(time, wr_time)
	prev_time = wks.cell(row, col).value

	embed = discord.Embed(
		title = track,
		color = green,
	)

	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.add_field(name='time', value=f'> {format_time(time)} (WR +{diff})', inline=False)

	# 記録が未登録の場合
	if prev_time is None:
		wks.update_cell(row, col, time)
		embed.add_field(name='your record', value='-')
		embed.set_footer(text='☑️ Update')
		return embed

	diff = calc_time_diff(prev_time, wr_time)
	embed.add_field(name='your record', value=f'> {format_time(prev_time)} (WR +{diff})', inline=False)

	if time < prev_time:
		wks.update_cell(row, col, time)
		embed.set_footer(text='☑️ Update')

	return embed


def show_record(
    author: discord.member.Member,
    server: str,
    track: str,
    row: int
    ) -> discord.Embed:
	wks = sh.worksheet(server)
	col = search_user(author, server)
	time = wks.cell(row, col).value
	wr_time = sh.worksheet('WR List').cell(row, WR_COL).value
	wrecorder = sh.worksheet('WR List').cell(row, PLAYER_COL).value

	embed = discord.Embed(
		title = track,
		color = green,
	)

	embed.set_thumbnail(url=get_thumbnail_url(row))

	if time is None:
		embed.add_field(name='time', value='-', inline=False)
	else:
		diff = calc_time_diff(time, wr_time)
		embed.add_field(name='time', value=f'> {format_time(time)} (WR +{diff})')
	
	embed.add_field(name='WR', value=f'> {format_time(wr_time)} (By {wrecorder})', inline=False)
	return embed


def show_sub_records(
    author: discord.member.Member,
    server: str,
    sub_time: str
    ) -> list[discord.Embed]:
	
	wks = sh.worksheet(server)
	col = search_user(author, server)
	user_name = str(author).split('#')[0]
	tracks = wks.col_values(TRACK_COL)
	wr_times = sh.worksheet('WR List').col_values(WR_COL)
	times = wks.col_values(col)
	
	embed_list = [discord.Embed(
			title = f"{user_name}'s records (sub: {sub_time[:3]}s)",
			color = green
		)]

	records = []
	for i in range(2, len(times)):
		if times[i] == '':
			continue

		diff = calc_time_diff(times[i], wr_times[i])
		sub_time_sec = float(sub_time)
		if sub_time_sec -1 < float(diff) <= sub_time_sec:
			records.append([diff, times[i], tracks[i]])
	
	records.sort()
	for i in range(len(records)):
		diff, time, track = records[i]

		# embedのfield数は最大25個
		if i == 25 or i == 50:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s records (sub: {sub_time[:3]}s)",
			color = green
			))
		
		embed_list[-1].add_field(name=f'{i+1}. {track}', value=f'> {format_time(time)} (WR +{diff})', inline=False)

	return embed_list


def show_all_records(author: discord.member.Member, server: str) -> list[discord.Embed]:
	wks = sh.worksheet(server)
	col = search_user(author, server)
	user_name = str(author).split('#')[0]
	tracks = wks.col_values(TRACK_COL)
	wr_times = sh.worksheet('WR List').col_values(WR_COL)
	records = wks.col_values(col)
	
	avg_diff = 0
	embed_list = [discord.Embed(
			title = f"{user_name}'s records",
			description = '[ワルハナNITA WR](https://docs.google.com/spreadsheets/d/e/' \
							'2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml)',
			color = green
		)]
	
	cnt = 0
	sub_tracks = [0]*5
	for i in range(2, len(records)):
		if records[i] == '':
			continue

		# embedのfield数は最大25個
		if cnt == 25 or cnt == 50:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s records",
				color = green
			))

		diff = calc_time_diff(records[i], wr_times[i])
		diff_int = int(diff[0])
		if diff_int < 5:
			sub_tracks[diff_int] += 1

		avg_diff += float(diff)
		embed_list[-1].add_field(name=tracks[i], value=f'> {format_time(records[i])} (WR +{diff})', inline=False)
		cnt = cnt + 1
	
	if cnt == 25 or cnt == 50:
		embed_list.append(discord.Embed(
			title = f"{user_name}'s records",
			color = green
		))

	# コースが未登録の場合を弾く
	if cnt != 0:
		avg_diff = '{:.3f}'.format(avg_diff / cnt)
		embed_list[-1].add_field(name='Average Diff', value=f'{avg_diff}s ({cnt} tracks)')
	
	# グラフの描画
	left = [1, 2, 3, 4, 5]
	plt.bar(left, sub_tracks, alpha=0.8)
	plt.xlabel('Sub Time')
	plt.ylabel('Tracks')
	plt.grid(linestyle='--', axis='y')
	buffer = BytesIO()
	plt.savefig(buffer, format='png', bbox_inches='tight')
	buffer.seek(0)
	plt.clf()
	plt.close()
	file = discord.File(buffer, filename='subGraph.png')
	embed_list[-1].set_image(url='attachment://subGraph.png')

	return embed_list, file


def show_wr(track: str, row: int):
	wks = sh.worksheet('RefSheet')
	track_num = row - 3
	embed = discord.Embed(
		title = f'WRs of {track}',
		color = green
	)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	recorder_col_list = ['E', 'J', 'O', 'T']
	time_col_list = ['F', 'K', 'P', 'U']
	recorder_col = recorder_col_list[track_num % 4]
	time_col = time_col_list[track_num % 4]
	start_row = 11 + (track_num // 4) * 13

	# テータの取得
	recorders = wks.range(f'{recorder_col}{start_row}:{recorder_col}{start_row+9}')
	times = wks.range(f'{time_col}{start_row}:{time_col}{start_row+9}')
	
	for i in range(10):
		embed.add_field(name=f'{i+1}. {recorders[i].value}', value=f'> {times[i].value}', inline=False)

	return embed


def track_records(server: str, track: str, row: int) -> discord.Embed:
	wks = sh.worksheet(server)
	user_list = wks.row_values(USER_ROW)
	time_list = wks.row_values(row)
	wr_time = sh.worksheet('WR List').cell(row, WR_COL).value
	embed = discord.Embed(
		title = track,
		color = green
	)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	records = []
	for i in range(1, len(time_list)):
		if time_list[i] == '':
			continue
		records.append([time_list[i], user_list[i]])

	avg_diff = 0
	records.sort()
	for i in range(len(records)):
		time, user = records[i]
		user_name = user.split('#')[0]
		diff = calc_time_diff(time, wr_time)
		avg_diff += float(diff)

		if i==0:
			user_name = f'🥇 {user_name}'
		elif i==1:
			user_name = f'🥈 {user_name}'
		elif i==2:
			user_name = f'🥉 {user_name}'
		else:
			user_name = f'{i+1}. {user_name}'

		embed.add_field(name=user_name, value=f'> {format_time(time)} (WR +{diff})', inline=False)
	
	if len(records) != 0:
		avg_diff = '{:.3f}'.format(avg_diff / len(records))
		embed.add_field(name='Average Diff', value=f'{avg_diff}s')

	return embed


def delete_record(
    author: discord.member.Member,
    server: str,
    track: str,
    row: int
    ) -> discord.Embed:
	wks = sh.worksheet(server)
	col = search_user(author, server)

	embed = discord.Embed(
		title = track,
		color = light_blue,
	)

	wks.update_cell(row, col, '')
	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.set_footer(text='☑️ Delete')

	return embed


def video_url(row: int) -> str:
	return sh.worksheet('WR List').cell(row, VIDEO_COL).value