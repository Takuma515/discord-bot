import os
import function
import discord
from discord.ext import commands


# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='_', intents=intents)


async def update_activity():
    activity = discord.Activity(name=f'{len(bot.guilds)} servers', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    


@bot.command(aliases=['s','S'])
async def set(ctx, *args):
    '''記録を登録'''
    await ctx.send(embed=function.set_record(ctx, args))


@bot.command(aliases=['r', 'R'])
async def record(ctx, *args):
    '''記録を表示'''
    embed_list, file = function.show_record(ctx, args)
    for i, embed in enumerate(embed_list):
        if i == len(embed_list) -1:
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(embed=embed)


@bot.command(aliases=['t', 'T'])
async def track(ctx, *args):
    '''指定コースの記録を表示'''
    await ctx.send(embed=function.track_records(ctx, args))


@bot.command(aliases=['tt', 'TT'])
async def tier_time(ctx, *args):
    '''tier別の平均タイムを表示'''
    await ctx.send(embed=function.tier_time(ctx, args))


@bot.command(aliases=['d', 'D'])
async def delete(ctx, *args):
    '''記録を削除'''
    await ctx.send(embed=function.delete_record(ctx, args))


@bot.command(aliases=['v', 'V'])
async def video(ctx, *args):
    '''解説動画のURLを送信'''
    await ctx.send(function.send_video_url(args))


@bot.command(aliases=['l', 'L'])
async def link(ctx):
    '''NITAスプシのURLを送信'''
    embed = discord.Embed(
        title = "NITA Links",
        description = '[150cc NITA リーダーボード](https://docs.google.com/spreadsheets/d/e/' \
                            '2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=0&single=true)\n' \
                      '[150cc NITA VSカスタムのみ](https://docs.google.com/spreadsheets/d/e/' \
                            '2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=406946200&single=true)'
    )
    await ctx.send(embed=embed)


# 一時停止
# @bot.command(aliases=['WR'])
# async def wr(ctx, *args):
#     await ctx.send(embed=function.show_wr(args))


# bot起動時
@bot.event
async def on_ready():
    print('ログインしました')
    await update_activity()


# サーバーに追加時
@bot.event
async def on_guild_join(guild):
    print(f'join "{guild}"')
    await update_activity()

 
@bot.command(aliases=['g', 'G'], hidden=True)
@commands.is_owner()
async def guilds(ctx):
    guild_names = sorted(g.name for g in bot.guilds)
    guilds = "\n".join(guild_names)

    embed = discord.Embed(
        title=f'{len(guild_names)} Servers',
        description=guilds
    )
    await ctx.send(embed=embed)


@bot.command(aliases=['ud'], hidden=True)
@commands.is_owner()
async def user_data(ctx):
    await ctx.send(embed = function.user_data())


# コマンドのエラー処理
@bot.event
async def on_command_error(ctx, error):
    if not ctx.guild:
        location = str(ctx.author)
    else:
        location = str(ctx.guild)
    
    log_message = f"{error} ({location})\nmessage: \"{ctx.message.content}\""
    print(log_message)

    if isinstance(error, commands.errors.CommandInvokeError):
        err_msg = "bot error"
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        err_msg = "error"
    
    await ctx.send(err_msg)



bot.run(os.environ['DISCORD_BOT_TOKEN'])