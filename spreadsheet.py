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
wks = sh.worksheet('UserData')

# 色の設定
err_color = 0xff3333
green = 0x00ff00
light_blue = 0x00ffff

# 行番号の設定
USER_ROW = 1
ID_ROW = 2
MMR_ROW = 3

# 列番号の設定
TRACK_COL = 1
PLAYER_COL = 2
WR_COL = 4
VIDEO_COL = 5

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
		wks.add_cols(1)
		wks.update_cell(ID_ROW, col, id)
		
	# ユーザ名の更新
	wks.update_cell(USER_ROW, col, author.name)

	return col


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


# タイムのフォーマット
def format_time(time: str) -> str:
	return time[0] + ':' + time[1] + time[2] + '.' + time[3:]


# サムネイルのURLを取得
def get_thumbnail_url(row: int) -> str:
	return f'https://raw.githubusercontent.com/Takuma515/discord-bot/main/images/{row-4}.png'


def set_record(
    author: discord.member.Member,
    time: str,
    track: str,
    row: int) -> discord.Embed:
	col = search_user(author)
	wr_time = wks.cell(row, WR_COL).value
	prev_time = wks.cell(row, col).value
	diff = calc_time_diff(time, wr_time)

	# WR以下 or WR+10秒以上の記録は弾く
	if not 0 < float(diff) <= 10:
		return discord.Embed(title='Input Error', description='Invalid value (Faster than WR or more than 10 seconds slower)', color=err_color)

	embed = discord.Embed(title = track, color = green)
	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.add_field(name='Input Time', value=f'> {format_time(time)} (WR +{diff})', inline=False)

	# 記録が未登録の場合
	if prev_time is None:
		wks.update_cell(row, col, time)
		embed.add_field(name='Your Record', value='-')
		embed.set_footer(text='☑️ Update')
		return embed

	diff = calc_time_diff(prev_time, wr_time)
	embed.add_field(name='Your Record', value=f'> {format_time(prev_time)} (WR +{diff})', inline=False)

	if time < prev_time:
		wks.update_cell(row, col, time)
		embed.set_footer(text='☑️ Update')

	return embed


def show_record(
    author: discord.member.Member,
    track: str,
    row: int
    ) -> discord.Embed:
	col = search_user(author)
	time = wks.cell(row, col).value
	wr_time = wks.cell(row, WR_COL).value
	wrecorder = wks.cell(row, PLAYER_COL).value
	time_list = sorted([x for x in wks.row_values(row)[6:] if x != ''])

	embed = discord.Embed(title = track, color = green)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	if time is None:
		embed.add_field(name='Your Time', value='-', inline=False)
		embed.add_field(name='WR', value=f'> {format_time(wr_time)} (By {wrecorder})', inline=False)
		return [embed], None
	
	diff = calc_time_diff(time, wr_time)
	embed.add_field(name='Your Time', value=f'> {format_time(time)} (WR +{diff})')
	embed.add_field(name='WR', value=f'> {format_time(wr_time)} (By {wrecorder})', inline=False)

	# ランクの表示
	rank = time_list.index(time) + 1
	if rank == 1:
		rank = '🥇 1st'
	elif rank == 2:
		rank = '🥈 2nd'
	elif rank == 3:
		rank = '🥉 3rd'
	else:
		rank = f'{rank}th'	
	embed.add_field(name='Rank', value=f'> {rank} ({len(time_list)} players)', inline=False)

	# タイムの分布を表示
	diff_records_count = [0]*5
	diff_time_list = [1, 2, 3, 4, 5]
	for t in time_list:
		diff = float(calc_time_diff(t, wr_time))
		for i in range(5):
			if diff <= diff_time_list[i]:
				diff_records_count[i] += 1
				break

	# グラフの作成
	color_list = ['cornflowerblue']*5
	diff = float(calc_time_diff(time, wr_time))
	for i in range(5):
		if diff <= diff_time_list[i]:
			color_list[i] = '#CC6677'
			break

	plt.bar(diff_time_list, diff_records_count, width=0.7, color=color_list, alpha=0.9)
	plt.xlabel('Time Diff from WR')
	plt.ylabel('Players')
	plt.grid(linestyle='--', axis='y')
	buffer = BytesIO()
	plt.savefig(buffer, format='png', bbox_inches='tight')
	buffer.seek(0)
	plt.clf()
	plt.close()
	file = discord.File(buffer, filename='subGraph.png')
	embed.set_image(url='attachment://subGraph.png')

	return [embed], file


def show_sub_records(
    author: discord.member.Member,
    sub_time: str
    ) -> list[discord.Embed]:
	
	col = search_user(author)
	user_name = author.name
	tracks = wks.col_values(TRACK_COL)
	wr_times = wks.col_values(WR_COL)
	user_times = wks.col_values(col)
	
	embed_list = [discord.Embed(
			title = f"{user_name}'s Records (sub: {sub_time[:3]}s)",
			color = green
		)]

	records = []
	for i in range(3, len(user_times)):
		if user_times[i] == '':
			continue

		diff = calc_time_diff(user_times[i], wr_times[i])
		sub_time_sec = float(sub_time)
		if sub_time_sec -1 < float(diff) <= sub_time_sec:
			records.append([diff, user_times[i], tracks[i]])
	
	records.sort()
	for i in range(len(records)):
		diff, time, track = records[i]

		# embedのfield数は最大25個
		if i == 25 or i == 50:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s Records (sub: {sub_time[:3]}s)",
			color = green
			))
		
		embed_list[-1].add_field(name=f'{i+1}. {track}', value=f'> {format_time(time)} (WR +{diff})', inline=False)

	return embed_list


def show_user_records(author: discord.member.Member) -> list[discord.Embed]:
	col = search_user(author)
	user_name = author.name
	tracks = wks.col_values(TRACK_COL)
	wr_times = wks.col_values(WR_COL)
	records = wks.col_values(col)
	
	avg_diff = 0
	embed_list = [discord.Embed(
			title = f"{user_name}'s Records",
			description = '[150cc NITA Leaderboard](https://docs.google.com/spreadsheets/d/e' \
			'/2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=0&single=true)',
			color = green
		)]
	
	cnt = 0
	sub_tracks = [0]*5
	for i in range(3, len(records)):
		if records[i] == '':
			continue

		# embedのfield数は最大25個
		if cnt != 0 and cnt % 25 == 0:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s Records",
				color = green
			))

		diff = calc_time_diff(records[i], wr_times[i])
		diff_int = int(diff[0])
		if diff_int < 5:
			sub_tracks[diff_int] += 1

		avg_diff += float(diff)
		embed_list[-1].add_field(name=tracks[i], value=f'> {format_time(records[i])} (WR +{diff})', inline=False)
		cnt += 1
	
	if cnt != 0 and cnt % 25 == 0:
		embed_list.append(discord.Embed(
			title = f"{user_name}'s Records",
			color = green
		))

	# コースが未登録の場合を弾く
	if cnt != 0:
		avg_diff = '{:.3f}'.format(avg_diff / cnt)
		embed_list[-1].add_field(name='Average Diff', value=f'{avg_diff}s ({cnt} tracks)')
	
	# グラフの作成
	color = 'cornflowerblue'
	left = [1, 2, 3, 4, 5]
	plt.bar(left, sub_tracks, color=color, width=0.7)
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


def track_records(members_id_list: set, track: str, row: int) -> discord.Embed:
	user_list = wks.row_values(USER_ROW)
	id_list = wks.row_values(ID_ROW)
	time_list = wks.row_values(row)
	wr_time = wks.cell(row, WR_COL).value
	embed = discord.Embed(
		title = track,
		color = green
	)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	# サーバーに所属しているユーザのみ記録を取得する
	records = []
	for i in range(6, len(time_list)):
		# メンバーが所属していない場合
		if id_list[i] not in members_id_list:
			continue
		# タイムが登録されていない場合
		if time_list[i] == '':
			continue

		records.append([time_list[i], user_list[i]])

	avg_diff = 0
	records.sort()
	records_num = min(len(records), EMBED_LIMIT-1)
	for i in range(records_num):
		time, user_name = records[i]
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
	
	# 記録が0件の場合を除く
	if len(records) != 0:
		avg_diff = '{:.3f}'.format(avg_diff / records_num)
		embed.add_field(name='Average Diff', value=f'{avg_diff}s')

	return embed


def show_tier_time(author: discord.member.Member, track: str, row: int) -> discord.Embed:
	mmr_list = wks.row_values(MMR_ROW)
	time_list = wks.row_values(row)
	wr_time = wks.cell(row, WR_COL).value
	col = search_user(author)
	user_time = wks.cell(row, col).value
	
	embed = discord.Embed(
		title = f'Tier Time of {track}',
		color = green
	)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	tier_name = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Sapphire', \
		'Ruby', 'Diamond', 'Master', 'Grandmaster']
	tier_range = [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 17000, 10*5]
	tier_time = [[0] * 2 for _ in range(10)]	# [cnt, sum_time]

	# mmrごとにタイムを集計
	for i in range(min(len(mmr_list), len(time_list))):
		mmr = mmr_list[i]
		time = time_list[i]

		if mmr == '' or time == '':
			continue

		for j in range(len(tier_name)):
			min_mmr, max_mmr = tier_range[j], tier_range[j+1]

			if min_mmr <= int(mmr) < max_mmr:
				tier_time[j][0] += 1
				tier_time[j][1] += convert_time_into_seconds(time)
				break
	
	# embedの処理
	if user_time is None:
		embed.add_field(name='Your Time', value='-')
	else:
		embed.add_field(name='Your Time', value=f'> {format_time(user_time)} (WR +{calc_time_diff(user_time, wr_time)})')
		user_time = format_time(user_time)
	
	for i in range(len(tier_name)):
		cnt, sum_time = tier_time[i][0], tier_time[i][1]

		# tierの人数が0人だった場合
		if cnt == 0:
			embed.add_field(name=f'{tier_name[i]} (n={cnt})', value='-', inline=False)
			continue

		avg_time = convert_seconds_into_time(sum_time / cnt)
		diff = calc_time_diff(avg_time, wr_time)
		embed.add_field(name=f'{tier_name[i]} (n={cnt})', value=f'> {format_time(avg_time)} (WR +{diff})', inline=False)


	return embed
	

def delete_record(
    author: discord.member.Member,
    track: str,
    row: int
    ) -> discord.Embed:

	embed = discord.Embed(title = track, color = light_blue,)
	col = search_user(author)
	wks.update_cell(row, col, '')
	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.set_footer(text='☑️ Delete')

	return embed


def video_url(row: int) -> str:
	return wks.cell(row, VIDEO_COL).value


def show_wr(track: str, row: int):
	wks = sh.worksheet('WR List')
	track_num = row - 4
	embed = discord.Embed(
		title = f'WRs of {track}',
		color = green
	)
	embed.set_thumbnail(url=get_thumbnail_url(row))

	col_list = [['B', 'C', 'D'], ['E', 'F', 'G'], ['H', 'I', 'J'], ['K', 'L', 'M']]
	start = (track_num//4)*17 + 8
	end = start + 14
	l, m, r = col_list[track_num%4]

	# データの取得
	recorders = wks.range(f'{l}{start}:{l}{end}')
	times = wks.range(f'{m}{start}:{m}{end}')
	urls = wks.range(f'{r}{start}:{r}{end}')

	for i in range(len(recorders)):
		recorder = recorders[i].value
		time = times[i].value
		url = urls[i].value

		if recorder == '' or time == '' or url == '':
			continue

		embed.add_field(name=f'{i+1}. {recorder}', value=f'> [{time}]({url})', inline=False)
	
	
	return embed


def user_data() -> discord.Embed:
	mmr_list = wks.row_values(3)
	tier_name = ['Unrated', 'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Sapphire', \
		'Ruby', 'Diamond', 'Master', 'Grandmaster']
	tier_range = [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 17000, 10*5]
	user_num_list = [0] * 11

	# mmrごとにユーザ数を集計
	for mmr in mmr_list[6:]:
		if not mmr:
			user_num_list[0] += 1
			continue

		for j in range(len(tier_name)):
			min_mmr, max_mmr = tier_range[j], tier_range[j+1]

			if min_mmr <= int(mmr) < max_mmr:
				user_num_list[j+1] += 1
				break
	
	description = '\n'.join(f'{tier_name[i]}: {user_num_list[i]}' for i in range(len(user_num_list)))
	description += f'\nTotal: {sum(user_num_list)}'
	embed = discord.Embed(title = 'User Data', description = description)
	return embed