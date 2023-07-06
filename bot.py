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
    

# 記録の登録
@bot.command(aliases=['s','S'])
async def set(ctx, *args):
    await ctx.send(embed=function.set_record(ctx, args))


# 個人の記録の表示
@bot.command(aliases=['r', 'R'])
async def record(ctx, *args):
    embed_list, file = function.show_record(ctx, args)
    for i, embed in enumerate(embed_list):
        if i == len(embed_list) -1:
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(embed=embed)


# WRの表示
@bot.command(aliases=['WR'])
async def wr(ctx, *args):
    await ctx.send(embed=function.show_wr(args))


# コースの記録の表示
@bot.command(aliases=['t', 'T'])
async def track(ctx, *args):
    await ctx.send(embed=function.track_records(ctx, args))


# tier別平均タイムを表示
@bot.command(aliases=['tt', 'TT'])
async def tier_time(ctx, *args):
    await ctx.send(embed=function.tier_time(ctx, args))


# 記録の削除
@bot.command(aliases=['d', 'D'])
async def delete(ctx, *args):
    await ctx.send(embed=function.delete_record(ctx, args))


# 解説動画URLを送信
@bot.command(aliases=['v', 'V'])
async def video(ctx, *args):
    await ctx.send(function.send_video_url(args))


# リンクの送信
@bot.command(aliases=['l', 'L'])
async def link(ctx):
    embed = discord.Embed(
        title = "NITA Links",
        description = '[NITA ALL](https://docs.google.com/spreadsheets/u/1/d/e/'\
                        '2PACX-1vRDdedRm18RtIu2hB9l5WrbaClaIPnZAVh_Xf7IeGzmsOVHcNdjoD3VWo8EdMxJ7JKdtcbFnebLjCcV/pubhtml#)\n' \
                      '[ワルハナNITA](https://docs.google.com/spreadsheets/d/e/' \
						'2PACX-1vTOT3PJwMcMrOE--rBPV3Vz1SUegmpmpCtP8NzMQoxHljks2JDaYQ8H1pj4Pi0i5xOmnnS3eDAxc4zY/pubhtml)\n' \
                      '[中量トルネードNITA](https://docs.google.com/spreadsheets/d/e/' \
                        '2PACX-1vRz9qxcj06seMvQcOf7m49x_2yxeynIb5Q72UrVOEc-vJNtmUH8YomPMTDuHXAH5py_xyDn3RcPdUzo/pubhtml?gid=1908866215&single=true)\n' \
                      '[150cc NITA リーダーボード](https://docs.google.com/spreadsheets/d/e/' \
                        '2PACX-1vRBXBdqpurvBmR--bzj9RJmgr7HxAoWVZmlwmhaBK-LYf_BbXn8iAPdH-ogBtXiAwxlTkQgn45PkeRW/pubhtml?gid=0&single=true)'
    )
    await ctx.send(embed=embed)

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

    if isinstance(error, commands.errors.CommandNotFound):
        err_msg = "command not found"
    elif isinstance(error, commands.errors.CommandInvokeError):
        err_msg = "bot error"
    else:
        err_msg = "error"
    
    await ctx.send(err_msg)


# Botの起動とDiscordサーバーへの接続
bot.run(os.environ['DISCORD_BOT_TOKEN'])