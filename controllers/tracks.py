import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, format_diff, get_thumbnail_url, convert_time_into_seconds, convert_seconds_into_time


color_error = 0xff3333
color_green = 0x00ff00

IGNORE_SERVER = 1071251903649939476

def show_track_records(
    ctx: commands.Context,
    track: str
) -> discord.Embed:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_t track_name`",
        color = color_error
    )

    embed_ignore = discord.Embed(
        title = "Input Error",
        description = "This command is not available in this server",
        color = color_error
    )

    if ctx.guild.id == IGNORE_SERVER:
        return embed_ignore

    track_name, track_id = track_info.search(track)
    if track_name is None:
        return embed_err
    
    # サーバーに所属するメンバーのIDリストを作成
    members_id_list = set(map(lambda m: str(m.id), ctx.guild.members))

    # データの取得
    user_names, user_ids = sheet.fetch_user_list()
    track_records = sheet.fetch_track_records(track_id)
    _, wr_time, _ = sheet.fetch_wr_info(track_id)

    embed = discord.Embed(title = track_name, color = color_green)
    embed.set_thumbnail(url = get_thumbnail_url(track_id))

    
    # サーバーに所属するメンバーの記録を取得
    records = []
    for i in range(7, len(track_records)):
        # メンバーが所属していない場合
        if user_ids[i] not in members_id_list:
            continue

        # 記録が登録されていない場合
        if track_records[i] == '':
            continue
        
        records.append((track_records[i], user_names[i]))
    
    if len(records) == 0:
        return embed

    # embedに記録を追加
    avg_time = 0
    records.sort()
    records_num = min(len(records), 24)
    for i in range(records_num):
        time, user_name = records[i]
        diff = calc_time_diff(time, wr_time)
        avg_time += convert_time_into_seconds(time)

        if i==0:
            user_name = f'🥇 {user_name}'
        elif i==1:
            user_name = f'🥈 {user_name}'
        elif i==2:
            user_name = f'🥉 {user_name}'
        else:
            user_name = f'{i+1}. {user_name}'

        embed.add_field(name=user_name, value=f'> {format_time(time)} (WR {format_diff(diff)})', inline=False)
    
    avg_time = convert_seconds_into_time(avg_time / records_num)
    diff = calc_time_diff(avg_time, wr_time)
    embed.add_field(name='Avg. Time', value=f'> {format_time(avg_time)} (WR {format_diff(diff)})', inline=False)
    
    return embed