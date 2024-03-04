import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import get_thumbnail_url


color_error = 0xff3333
color_light_blue = 0x00ffff

# 記録の削除
def delete_record(
    ctx: commands.Context,
    track: str
) -> discord.Embed:
    
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_d track_name`",
        color = color_error
    )

    track_name, track_id = track_info.search(track)
    if track_name is None:
        return embed_err

    embed = discord.Embed(title = track_name, color = color_light_blue)
    sheet.delete_record(track_id, ctx.author)

    embed.set_thumbnail(url = get_thumbnail_url(track_id))
    embed.set_footer(text=f'Deleted by {ctx.author.name}')

    return embed