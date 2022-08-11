import discord
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import math

# 設定
file_name = 'NITA'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# スプレッドシートにアクセス
key = os.environ['API_KEY']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(key), scope)
gc = gspread.authorize(credentials)
sh = gc.open(file_name)

# 色の設定
green = 0x00ff00
light_blue = 0x00ffff 

# userを探して列番号を返す
def search_user(user, server):
	wks = sh.worksheet(server)
	user_list = wks.row_values(1)
	col = len(user_list) + 1

	if user in user_list:
		col = user_list.index(user) + 1
	else:
		# userが見つからなかったので登録する
		wks.update_cell(1, col, user)

	return col


# タイム差を計算
def calc_time_diff(t1, t2):
	t1_sec = float(t1[0])*60 + float(t1[1])*10 + float(t1[2]) + float(t1[3:]) / 1000
	t2_sec = float(t2[0])*60 + float(t2[1])*10 + float(t2[2]) + float(t2[3:]) / 1000
	return  t1_sec - t2_sec


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
	prev_time = wks.cell(row, col).value
	wr_time = wks.cell(row, 2).value
	diff = calc_time_diff(time, wr_time)

	embed = discord.Embed(
		title = track,
        color = green,
    )

	embed.set_thumbnail(url=get_thumbnail_url(row))
	embed.add_field(name='time', value=format_time(time) + ' (WR +' + '{:.3f}'.format(diff) + ')', inline=False)

	# 記録が未登録の場合
	if prev_time is None:
		wks.update_cell(row, col, time)
		embed.add_field(name='your record', value='-', inline=False)
		embed.set_footer(text='Updated', icon_url='http://drive.google.com/uc?export=view&id=1XX9DcXltWeQkPB0GNWqXSt6wIND6tAK6')
		return embed

	diff = calc_time_diff(time, prev_time)
	embed.add_field(name='your record', value=format_time(prev_time), inline=False)

	if diff < 0:
		wks.update_cell(row, col, time)
		embed.set_footer(text='Updated', icon_url='http://drive.google.com/uc?export=view&id=1XX9DcXltWeQkPB0GNWqXSt6wIND6tAK6')
	else:
		embed.set_footer(text='Not Updated', icon_url='http://drive.google.com/uc?export=view&id=1b6ch6PsbuUimPZVzNOhTh3cxrli71YJC')
	return embed



def show_record(user, server, track, row):
	wks = sh.worksheet(server)
	col = search_user(user, server)
	time = wks.cell(row, col).value
	wr_time = wks.cell(row, 2).value

	embed = discord.Embed(
		title = track,
        color = green,
    )

	embed.set_thumbnail(url=get_thumbnail_url(row))

	if time is None:
		embed.add_field(name='time', value='-', inline=False)
		embed.add_field(name='WR', value=format_time(wr_time), inline=False)
	else:
		diff = calc_time_diff(time, wr_time)
		embed.add_field(name='time', value=format_time(time) + ' (WR +' + '{:.3f}'.format(diff) + ')')

	return embed



def show_all_records(user, server):
	wks = sh.worksheet(server)
	col = search_user(user, server)
	user_name = user.split('#')[0]
	tracks = wks.col_values(1)
	wr = wks.col_values(2)
	records = wks.col_values(col)
	embed_list = [discord.Embed(
			title = f"{user_name}'s records",
			description = '[ワルハナNITA WR](https://docs.google.com/spreadsheets/d/e/2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml)',
        	color = green
    	)]
	
	cnt = 0
	sub_list = [0]*5
	for i in range(1, len(records)):
		if records[i] == '':
			continue

		if cnt == 25 or cnt == 50:
			embed_list.append(discord.Embed(
				title = f"{user_name}'s records",
				description = '[ワルハナNITA WR](https://docs.google.com/spreadsheets/d/e/2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml)',
        		color = green
    		))

		diff = calc_time_diff(records[i], wr[i])
		if diff <= 5:
			sub_idx = math.floor(diff)
			sub_list[sub_idx] = sub_list[sub_idx] + 1
		
		embed_list[-1].add_field(name=tracks[i], value='> ' + format_time(records[i]) + ' (WR +' + '{:.3f}'.format(diff) + ')', inline=False)
		cnt = cnt + 1

	return embed_list


def track_records(server, track, row):
	wks = sh.worksheet(server)
	users = wks.row_values(1)
	time_list = wks.row_values(row)
	wr_time = wks.cell(row, 2).value

	embed = discord.Embed(
		title = track,
        color = green,
    )

	embed.set_thumbnail(url=get_thumbnail_url(row))

	records = []
	for i in range(2, len(time_list)):
		if time_list[i] == '':
			continue
		records.append([time_list[i], users[i]])

	
	records.sort()
	for i in range(len(records)):
		time, user = records[i]
		diff = calc_time_diff(time, wr_time)
		embed.add_field(name=user.split('#')[0], value='> ' + format_time(time)  + ' (WR +' + '{:.3f}'.format(diff) + ')', inline=False)

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