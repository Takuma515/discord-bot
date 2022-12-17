import discord
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

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
TRACK_COL = 1
PLAYER_COL = 2
WR_COL = 4
VIDEO_COL = 5

# userを探して列番号を返す
def search_user(user, server):
	wks = sh.worksheet(server)
	user_list = wks.row_values(USER_ROW)
	col = len(user_list) + 1

	if user in user_list:
		col = user_list.index(user) + 1
	else:
		# userが見つからなかったので登録する
		wks.update_cell(1, col, user)

	return col


# タイムを秒に変換
def convert_time_into_seconds(time):
	return float(time[0])*60 + float(time[1])*10 + float(time[2]) + float(time[3:]) / 1000


# タイム差を計算
def calc_time_diff(time1, time2):
	t1_sec = convert_time_into_seconds(time1)
	t2_sec = convert_time_into_seconds(time2)
	return '{:.3f}'.format(t1_sec - t2_sec)


# タイムのフォーマット
def format_time(time):
	return time[0] + ':' + time[1] + time[2] + '.' + time[3:]


# サムネイルのURLを取得
def get_thumbnail_url(row):
	if row < 50:
		# 旧コース
		track_id1 = (row-2) // 4 + 1
		track_id2 = (row-1) - (track_id1-1) * 4
		return f'https://www.nintendo.co.jp/switch/aabpa/assets/images/course/thumbnail/{track_id1}-{track_id2}.jpg'
	else:
		# 新コース
		vol = (row - 50) // 8 + 1
		cup = ((row - 2) % 8) // 4 + 1
		cover = (row - 2) % 4 + 1
		return f'https://www.nintendo.co.jp/switch/aabpa/assets/images/coursepack/lineup/vol0{vol}/vol0{vol}_cup0{cup}_cover0{cover}.jpg'


def set_record(user, time, server, track, row):
	wks = sh.worksheet(server)
	col = search_user(user, server)
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
		embed.set_footer(text='Updated')
		return embed

	diff = calc_time_diff(prev_time, wr_time)
	embed.add_field(name='your record', value=f'> {format_time(prev_time)} (WR +{diff})', inline=False)

	if time < prev_time:
		wks.update_cell(row, col, time)
		# embed.set_footer(text='Updated', icon_url='http://drive.google.com/uc?export=view&id=1XX9DcXltWeQkPB0GNWqXSt6wIND6tAK6')
		embed.set_footer(text='Update✔︎')

	return embed


def show_record(user, server, track, row):
	wks = sh.worksheet(server)
	col = search_user(user, server)
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


def show_sub_records(user, server, sub_time):
	wks = sh.worksheet(server)
	col = search_user(user, server)
	user_name = user.split('#')[0]
	tracks = wks.col_values(TRACK_COL)
	wr_times = sh.worksheet('WR List').col_values(WR_COL)
	times = wks.col_values(col)
	
	embed_list = [discord.Embed(
			title = f"{user_name}'s records (sub: {sub_time[:3]}s)",
        	color = green
    	)]

	records = []
	for i in range(1, len(times)):
		if times[i] == '':
			continue
		diff = calc_time_diff(times[i], wr_times[i])
		if diff <= sub_time:
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


def show_all_records(user, server):
	wks = sh.worksheet(server)
	col = search_user(user, server)
	user_name = user.split('#')[0]
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
	for i in range(1, len(records)):
		if records[i] == '':
			continue

		# embedのfield数は最大25個
		if cnt == 25 or cnt == 50:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s records",
        		color = green
    		))

		diff = calc_time_diff(records[i], wr_times[i])
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
	
	return embed_list


def track_records(server, track, row):
	wks = sh.worksheet(server)
	users = wks.row_values(USER_ROW)
	times = wks.row_values(row)
	wr_time = sh.worksheet('WR List').cell(row, WR_COL).value
	embed = discord.Embed(
		title = track,
        color = green
    )
	embed.set_thumbnail(url=get_thumbnail_url(row))

	records = []
	for i in range(1, len(times)):
		if times[i] == '':
			continue
		records.append([times[i], users[i]])

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


def delete_record(user, server, track, row):
	wks = sh.worksheet(server)
	col = search_user(user, server)

	embed = discord.Embed(
		title = track,
        color = light_blue,
    )

	wks.update_cell(row, col, '')
	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.set_footer(text='Deleted')

	return embed


def video_url(row):
	return sh.worksheet('WR List').cell(row, VIDEO_COL).value