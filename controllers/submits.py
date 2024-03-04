import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, get_thumbnail_url


color_error = 0xff3333
color_green = 0x00ff00

def submit_record(
    ctx: commands.Context,
    track: str,
    time: str
) -> discord.Embed:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_s mks 140123`",
        color = color_error
    )

    track_name, track_id = track_info.search(track)
    if track_name is None:
        return embed_err
    
    if len(time) != 6 or time[0] == '0' or not time.isdecimal():
        return embed_err

    # データの取得
    col_id = sheet.search_user(ctx.author)
    prev_time = sheet.fetch_user_record(track_id, col_id)
    _, wr_time, _ = sheet.fetch_wr_info(track_id)

    diff = calc_time_diff(time, wr_time)
    if not 0 < float(diff) <= 10:
        return discord.Embed(title='Input Error', description='Invalid value (Faster than WR or more than 10 seconds slower)', color=color_error)


    # embedの設定
    embed = discord.Embed(title = track_name, color = color_green)
    embed.set_thumbnail(url = get_thumbnail_url(track_id))
    embed.add_field(name='Input Time', value=f'> {format_time(time)} (WR +{diff})', inline=False)


    # 記録が未登録の場合
    is_update = False
    if prev_time is None:
        embed.add_field(name='Your Record', value='-')
        is_update = True
    else:
        diff = calc_time_diff(prev_time, wr_time)
        embed.add_field(name='Your Record', value=f'> {format_time(prev_time)} (WR +{diff})', inline=False)
        is_update = time < prev_time
    
    # データの更新
    if is_update:
        sheet.update_record(track_id, col_id, time)
        embed.set_footer(text=f'☑️ Updated by {ctx.author.name}')

    return embed