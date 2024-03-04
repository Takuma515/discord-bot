import discord
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, get_thumbnail_url


color_error = 0xff3333
color_green = 0x00ff00


def show_wr(
    track: str
) -> discord.Embed:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_wr track_name`",
        color = color_error
    )

    track_name, track_id = track_info.search(track)
    if track_name is None:
        return embed_err
    
    players, times, urls = sheet.fetch_wr_list(track_id)

    embed = discord.Embed(
        title = f'WR of {track_name}',
        color = color_green
    )
    embed.set_thumbnail(url = get_thumbnail_url(track_id))

    wr_time = times[0].value.replace(':', '').replace('.', '')
    for i in range(len(players)):
        player = players[i].value
        if player == '':
            break
        time = times[i].value
        url = urls[i].value
        diff = calc_time_diff(time.replace(':', '').replace('.', ''), wr_time)
        embed.add_field(name=f'{i+1}. {player}', value=f'> [{time} (WR +{diff})]({url})', inline=False)

    return embed