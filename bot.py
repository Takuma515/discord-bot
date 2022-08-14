from ast import alias
from email import message
import os
import function
from discord.ext import commands

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='_')

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
    await ctx.send(function.send_video(ctx, args))


# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send("にゃーん")



# Botの起動とDiscordサーバーへの接続
bot.run(os.environ['DISCORD_BOT_TOKEN'])