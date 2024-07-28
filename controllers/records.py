import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from io import BytesIO
import track_info
import rank_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, format_diff, get_thumbnail_url


color_error = 0xff3333
color_green = 0x00ff00
color_light_blue = 0x00ffff

IGNORE_SERVER = 1071251903649939476


def show_record(
    ctx: commands.Context,
    arg: str
) -> tuple[list[discord.Embed], discord.File]:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_r track_name` or `_r username` or `_r number`",
        color = color_error
    )

    embed_ignore = discord.Embed(
        title = "Input Error",
        description = "This command is not available in this server",
        color = color_error
    )

    embed_list = [embed_err]
    file = None

    # argによって処理を分岐
    if arg is None:
        return show_user_records(ctx.author)
    
    sub_list = ['1', '2', '3', '4', '5']
    track_name, track_id = track_info.search(arg)
    is_user_exist = ctx.guild is not None and ctx.guild.get_member_named(arg) is not None
    rank_id = rank_info.search(arg)

    if arg in sub_list:
        embed_list = show_sub_records(ctx.author, arg)
    elif track_name is not None:
        embed_list, file = show_track_record(ctx.author, track_name, track_id)
    elif is_user_exist:
        if ctx.guild.id == IGNORE_SERVER:
            return [embed_ignore], None
        embed_list, file = show_user_records(ctx.guild.get_member_named(arg))
    elif rank_id != -1:
        embed_list = show_rank_records(ctx.author, rank_id)

    return embed_list, file


# ユーザーの指定コースの記録を表示
def show_track_record(
    author: discord.member.Member,
    track_name: str,
    track_id: int
) -> tuple[list[discord.Embed], discord.File]:
    
    col_id = sheet.search_user(author)
    user_name = author.name
    user_time = sheet.fetch_record_by_user(track_id, col_id)
    wr_player, wr_time, wr_link = sheet.fetch_wr_info(track_id)
    track_records = sheet.fetch_track_records(track_id)
    track_records = sorted([record for record in track_records[7:] if record != ''])

    embed = discord.Embed(title = track_name, color = color_green)
    embed.set_thumbnail(url=get_thumbnail_url(track_id))

    if user_time is None:
        embed.add_field(name='Your Record', value='-')
        embed.add_field(name='WR', value=f'> [{format_time(wr_time)} (By {wr_player})]({wr_link})', inline=False)
        return [embed], None
    
    diff = calc_time_diff(user_time, wr_time)
    embed.add_field(name='Your Record', value=f'> {format_time(user_time)} (WR {format_diff(diff)})', inline=False)
    embed.add_field(name='WR', value=f'> [{format_time(wr_time)} (By {wr_player})]({wr_link})', inline=False)
    embed.set_footer(text=f"{user_name}'s Record")

    # ランクの表示
    rank = track_records.index(user_time) + 1
    if rank == 1:
        rank = '🥇 st'
    elif rank == 2:
        rank = '🥈 nd'
    elif rank == 3:
        rank = '🥉 rd'
    else:
        rank = f'{rank}'

    embed.add_field(name='Rank', value=f'> {rank} ({len(track_records)} players)', inline=False)

    # タイムの分布リストを作成
    sub_records_count = [0]*5
    sub_time_list = [1, 2, 3, 4, 5]
    for record in track_records:
        diff = float(calc_time_diff(record, wr_time))
        for i in range(5):
            if diff <= sub_time_list[i]:
                sub_records_count[i] += 1
                break

    # グラフの作成
    color_list = ['cornflowerblue']*5
    diff = float(calc_time_diff(user_time, wr_time))
    for i in range(5):
        if diff <= sub_time_list[i]:
            color_list[i] = '#CC6677'
            break

    plt.bar(sub_time_list, sub_records_count, color=color_list, width=0.7)
    plt.xlabel('Sub Time')
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


# ユーザの全ての記録を表示
def show_user_records(
    author: discord.member.Member
) -> tuple[list[discord.Embed], discord.File]:

    user_name = author.name
    tracks = sheet.fetch_track_name()
    records = sheet.fetch_records_by_user(sheet.search_user(author))
    _, wr_times, _ = sheet.fetch_all_wr_info()

    embed_list = [discord.Embed(
        title = f'{user_name}\'s Records',
        color = color_green
    )]

    # embedの処理
    avg_diff = 0
    records_cnt = 0
    sub_tracks = [0]*5
    for i in range(3, len(records)):
        if records[i] == '':
            continue

        # embedのfield数は25個まで
        if records_cnt != 0 and records_cnt % 25 == 0:
            embed_list.append(discord.Embed(
                title = f'{user_name}\'s Records',
                color = color_green
            ))
        
        diff = calc_time_diff(records[i], wr_times[i])
        for j in range(1, 6):
            if float(diff) <= j:
                sub_tracks[j-1] += 1
                break
        
        embed_list[-1].add_field(name=f'{tracks[i]}', value=f'> {format_time(records[i])} (WR {format_diff(diff)})', inline=False)

        avg_diff += float(diff)
        records_cnt += 1
    
    # 記録が未登録の場合
    if records_cnt == 0:
        return embed_list, None

    # embedのfield数は25個まで
    if records_cnt % 25 == 0:
        embed_list.append(discord.Embed(
			title = f"{user_name}'s Records",
			color = color_green
		))

    # 平均タイム差
    avg_diff = '{:.3f}'.format(avg_diff / records_cnt)
    embed_list[-1].add_field(name='Avg. Diff.', value=f'> {avg_diff}s ({records_cnt} tracks)')

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


# 指定のsubタイムの記録を表示
def show_sub_records(
    author: discord.member.Member,
    sub_time: str
) -> list[discord.Embed]:
    
    col_id = sheet.search_user(author)
    user_name = author.name
    tracks = sheet.fetch_track_name()
    _, wr_times, _ = sheet.fetch_all_wr_info()
    records = sheet.fetch_records_by_user(col_id)

    embed_list = [discord.Embed(
			title = f"{user_name}'s Records (sub: {sub_time}.0s)",
			color = color_green
	)]

    
    sub_records = []
    for i in range(3, len(records)):
        if records[i] == '':
            continue

        diff = calc_time_diff(records[i], wr_times[i])

        if int(sub_time) -1 < float(diff) <= int(sub_time):
            sub_records.append([diff, records[i], tracks[i]])
        elif sub_time == '1' and float(diff) <= 0:
            sub_records.append([diff, records[i], tracks[i]])
    
    sub_records.sort()
    for i in range(len(sub_records)):
        diff, time, track = sub_records[i]

        # embedのfield数は25個まで
        if i != 0 and i % 25 == 0:
            embed_list.append(discord.Embed(
                title = f"{user_name}'s Records (sub: {sub_time}.0s)",
                color = color_green
            ))
        
        embed_list[-1].add_field(name=f'{i+1}. {track}', value=f'> {format_time(time)} (WR {format_diff(diff)})', inline=False)
    
    return embed_list


# ユーザの指定ランクの中央値との差を表示
def show_rank_records(
    author: discord.member.Member,
    rank_id: int
) -> list[discord.Embed]:
    
    user_name = author.name
    tracks = sheet.fetch_track_name()
    records = sheet.fetch_records_by_user(sheet.search_user(author))
    rank_times = sheet.fetch_rank_times(rank_id)
    rank_color = rank_info.rank_color(rank_id)

    embed_list = [discord.Embed(
        title = f'{user_name}\'s Records (rank: {rank_info.rank_name(rank_id)})',
        color = rank_color
    )]

    # embedの処理
    avg_diff = 0
    records_cnt = 0
    for i in range(3, min(len(records), len(rank_times))):
        if records[i] == '' or rank_times[i] == '':
            continue
        
        # embedのfield数は25個まで
        if records_cnt != 0 and records_cnt % 25 == 0:
            embed_list.append(discord.Embed(
                title = f'{user_name}\'s Records (rank: {rank_info.rank_name(rank_id)})',
                color = rank_color
            ))

        diff = calc_time_diff(records[i], rank_times[i])
        embed_list[-1].add_field(name=f'{tracks[i]}', value=f'> {format_time(records[i])} (tier med {format_diff(diff)})', inline=False)
        
        avg_diff += float(diff)
        records_cnt += 1
    
    # 記録が未登録の場合
    if records_cnt == 0:
        return embed_list
    
    # embedのfield数は25個まで
    if records_cnt % 25 == 0:
        embed_list.append(discord.Embed(
            title = f"{user_name}'s Records (rank: {rank_info.rank_name(rank_id)})",
            color = rank_color
        ))
    
    # 平均タイム差
    avg_diff = '{:.3f}'.format(avg_diff / records_cnt)
    embed_list[-1].add_field(name='Avg. Diff.', value=f'> {avg_diff}s ({records_cnt} tracks)')

    return embed_list