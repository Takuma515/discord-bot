import discord
from discord.ext import commands
from discord import app_commands
import logging
import os
from controllers import deletes, submits, wrs, videos, records, tracks, tier_times, users_data


# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

class NitaBot(commands.AutoShardedBot):
    def __init__(self, command_prefix=commands.when_mentioned_or("_"), *, intents: discord.Intents = intents) -> None:
        super().__init__(
            command_prefix,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self) -> None:
        await bot.tree.sync()


bot = NitaBot(intents=intents)


@bot.event
async def on_ready():
    print('ログインしました')
    await bot.change_presence(
        activity=discord.Activity(
            status=discord.Status.online,
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers"
        )
    )


@bot.event
async def on_guild_join(guild: discord.Guild):
    await bot.change_presence(
        activity=discord.Activity(
            status=discord.Status.online,
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers"
        )
    )


@bot.hybrid_command(
    aliases=['s', 'S'],
    description='記録を登録する'
)
@app_commands.describe(
    track='例: マリカス',
    time='例: 140123'
)
async def submit(
    ctx: commands.Context,
    track: str,
    time: str
) -> None:
    '''記録を登録する'''

    await ctx.defer()
    await ctx.send(embed=submits.submit_record(ctx, track, time))


@bot.hybrid_command(
    aliases=['r', 'R'],
    description='記録を表示する'
)
@app_commands.describe(arg='コース名、ユーザー名、数字のいずれかを指定する')
async def record(
    ctx: commands.Context,
    *,
    arg: str = None
) -> None:
    '''記録を表示する'''

    await ctx.defer()

    embed_list, file = records.show_record(ctx, arg)
    for i, embed in enumerate(embed_list):
        if i == len(embed_list) -1:
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(embed=embed)


@bot.hybrid_command(
    aliases=['d', 'D'],
    description='記録を削除する'
)
@app_commands.describe(track='例: マリカス')
async def delete(
    ctx: commands.Context,
    track: str
) -> None:
    '''記録を削除する'''

    await ctx.defer()
    await ctx.send(embed=deletes.delete_record(ctx, track))


# @bot.hybrid_command(
#     aliases=['t', 'T'],
#     description='指定コースの記録を表示する'
# )
# @app_commands.describe(track='例: マリカス')
# async def track(
#     ctx: commands.Context,
#     track: str
# ) -> None:
#     '''指定コースの記録を表示する'''

#     await ctx.defer()
#     await ctx.send(embed=tracks.show_track_records(ctx, track))


@bot.hybrid_command(
    aliases=['tt', 'TT'],
    description='tierごとの平均タイムを表示する'
)
@app_commands.describe(track='例: マリカス')
async def tier_time(
    ctx: commands.Context,
    track: str
) -> None:
    '''tierごとの平均タイムを表示する'''

    await ctx.defer()
    await ctx.send(embed=tier_times.show_tier_time(ctx, track)
)



@bot.hybrid_command(
    aliases=['w', 'W', 'WR'],
    description='WRを表示する'
)
@app_commands.describe(track='例: マリカス')
async def wr(
    ctx: commands.Context,
    track: str
) -> None:
    '''WRを表示する'''

    await ctx.defer()
    await ctx.send(embed=wrs.show_wr(track))


@bot.hybrid_command(
    aliases=['v', 'V'],
    description='解説動画のリンクを送信する'
)
@app_commands.describe(track='例: マリカス')
async def video(
    ctx: commands.Context,
    track: str
) -> None:
    '''解説動画のリンクを送信する'''

    await ctx.defer()
    await ctx.send(videos.send_video_url(track))


@bot.hybrid_command(
    aliases=['l', 'L'],
    description='NITAのリーダーボードのリンクを送信する'
)
async def leaderboard(
    ctx: commands.Context
) -> None:
    '''NITAのリーダーボードのリンクを送信する'''

    embed = discord.Embed(
        title = "150cc NITA Links",
        description = '[リーダーボード (Leaderboard)](https://docs.google.com/spreadsheets/d/e/' \
                            '2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=0&single=true)\n' \
                        '[全てのカスタム (All Combinations)](https://docs.google.com/spreadsheets/d/e' \
                            '/2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=228689205&single=true)\n' \
                        '[VSカスタムのみ (Meta Only)](https://docs.google.com/spreadsheets/d/e/' \
                            '2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=406946200&single=true)'
    )
    await ctx.send(embed=embed)


@bot.hybrid_command(
    aliases=['ud'],
    description='ユーザーのmmr分布を表示する')
async def user_data(ctx):
    await ctx.send(embed = users_data.show_user_data())


# @bot.hybrid_command(
#     aliases=['g', 'G'],
#     hidden=True
# )
# @commands.is_owner()
# async def guilds(ctx):
#     guild_names = sorted(g.name for g in bot.guilds)
#     guilds = "\n".join(guild_names)

#     embed = discord.Embed(
#         title=f'{len(guild_names)} Servers',
#         description=guilds
#     )
#     await ctx.send(embed=embed)


# コマンドのエラー処理
@bot.event
async def on_command_error(ctx, error):
    if not ctx.guild:
        location = str(ctx.author)
    else:
        location = str(ctx.guild)
    
    log_message = f"{error} ({location})\nmessage: \"{ctx.message.content}\""
    args = ctx.args
    print(log_message)
    print(f"args: {args}")

    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Missing required argument")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send("Bad argument")
    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("bot error")
    else:
        await ctx.send("error")
    raise error


bot.run(token=os.environ['DISCORD_BOT_TOKEN'], log_level=logging.WARNING)