import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, format_diff, get_thumbnail_url, convert_full_to_half


color_error = 0xFF3333
color_green = 0x00FF00
color_wr = 0xA3022C

AUTHORIZED_USERS = [743511873978105916, 387192800451756033, 689845214273339589]

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

    time = convert_full_to_half(time)

    # データの取得
    col_id = sheet.search_user(ctx.author)
    prev_time = sheet.fetch_record_by_user(track_id, col_id)
    _, wr_time, _ = sheet.fetch_wr_info(track_id)

    diff = calc_time_diff(time, wr_time)
    if not -2 <= float(diff) <= 10:
        embed_err.description = 'Invalid value (more than 2 seconds faster or 10 seconds slower than WR)'
        return embed_err
    
    if float(diff) < 0 and ctx.author.id not in AUTHORIZED_USERS:
        embed_err.description = 'Please contact bot owner to submit a faster record than WR'
        return embed_err


    # embedの設定
    embed = discord.Embed(title = track_name, color = color_green)
    embed.set_thumbnail(url = get_thumbnail_url(track_id))
    embed.add_field(name='Input Time', value=f'> {format_time(time)} (WR {format_diff(diff)})', inline=False)

    if diff[0] == '-':
        embed.color = color_wr
        embed.description = '[NITA Submission Form](https://docs.google.com/forms/d/e/' \
        '1FAIpQLScEeKCItXjuSZQb2F2biwu9_Re3Rq9ts7lgAg5uQIwYPfmhPw/viewform)'


    # 記録が未登録の場合
    is_update = False
    if prev_time is None:
        embed.add_field(name='Your Record', value='-')
        is_update = True
    else:
        diff = calc_time_diff(prev_time, wr_time)
        embed.add_field(name='Your Record', value=f'> {format_time(prev_time)} (WR {format_diff(diff)})', inline=False)
        is_update = time < prev_time
    
    # データの更新
    if is_update:
        sheet.update_record(track_id, col_id, time)
        embed.set_footer(text=f'☑️ Updated by {ctx.author.name}')

    return embed