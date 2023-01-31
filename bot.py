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
    embed_list = function.show_record(ctx, args)
    for embed in embed_list:
        await ctx.send(embed=embed)


# コースの記録の表示
@bot.command(aliases=['t', 'T'])
async def track(ctx, *args):
    await ctx.send(embed=function.track_records(ctx, args))


# 記録の削除
@bot.command(aliases=['d', 'D'])
async def delete(ctx, *args):
    await ctx.send(embed=function.delete_record(ctx, args))


# 解説動画URLを送信
@bot.command(aliases=['v', 'V'])
async def video(ctx, *args):
    await ctx.send(function.send_video_url(args))


# bot起動時に動作
@bot.event
async def on_ready():
    print('ログインしました')


# サーバーに追加されたとき
@bot.event
async def on_guild_join(guild):
    print(f'join "{guild}"')


# コマンドのエラー
@bot.event
async def on_command_error(ctx, error):
    print(f'{error} ({ctx.guild})')
    err_msg = "error"
    if isinstance(error, commands.errors.CommandNotFound):
        err_msg = "コマンドが存在しません"
    elif isinstance(error, commands.errors.CommandInvokeError):
        err_msg = "このbotを使用するにはチームを登録する必要があります。" \
            "botの作成者 (taku#3173) までご連絡ください。"
    
    await ctx.send(err_msg)


# Botの起動とDiscordサーバーへの接続
bot.run(os.environ['DISCORD_BOT_TOKEN'])