import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, format_diff, get_thumbnail_url, convert_time_into_seconds, convert_seconds_into_time


color_error = 0xff3333
color_green = 0x00ff00


def show_tier_time(
    ctx: commands.Context,
    track: str
) -> discord.Embed:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_tt track_name`",
        color = color_error
    )

    track_name, track_id = track_info.search(track)
    if track_name is None:
        return embed_err
    
    mmr_list = sheet.fetch_mmr_list()
    track_records = sheet.fetch_track_records(track_id)
    _, wr_time, _ = sheet.fetch_wr_info(track_id)

    embed = discord.Embed(title = f'Tier Time of {track_name}', color = color_green)
    embed.set_thumbnail(url = get_thumbnail_url(track_id))

    tier_name = ['Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Sapphire', \
        'Ruby', 'Diamond', 'Master', 'Grandmaster']
    tier_range = [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 17000, 10*5]
    tier_time_info = [[0] * 2 for _ in range(10)]	# [cnt, sum_time]

    # tierごとにタイムを集計
    for i in range(min(len(mmr_list), len(track_records))):
        mmr = mmr_list[i]
        record = track_records[i]
        if mmr == '' or record == '':
            continue

        
        for j in range(len(tier_name)):
            min_mmr, max_mmr = tier_range[j], tier_range[j+1]
            
            if min_mmr <= int(mmr) < max_mmr:
                tier_time_info[j][0] += 1
                tier_time_info[j][1] += convert_time_into_seconds(record)
                break
    
    col_id = sheet.search_user(ctx.author)
    user_time = sheet.fetch_user_record(track_id, col_id)

    # embedに追加
    if user_time is None:
        embed.add_field(name='Your Record', value='-')
    else:
        diff = calc_time_diff(user_time, wr_time)
        embed.add_field(name='Your Record', value=f'> {format_time(user_time)} (WR {format_diff(diff)})', inline=False)
    
    for i in range(len(tier_name)):
        cnt, sum_time = tier_time_info[i]

        if cnt == 0:
            embed.add_field(name=f'{tier_name[i]} / N = {cnt}', value='-', inline=False)
            continue

        avg_time = convert_seconds_into_time(sum_time / cnt)
        diff = calc_time_diff(avg_time, wr_time)
        embed.add_field(name=f'{tier_name[i]} / N = {cnt}', value=f'> {format_time(avg_time)} (WR {format_diff(diff)})', inline=False)

    
    return embed