import discord
from discord.ext import commands

import track
import spreadsheet

err_color = 0xff3333

# 記録の登録
def set_record(ctx: commands.Context, args: list[str]) -> discord.Embed:
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_s ttc 150123`",
        color = err_color
    )

    # 入力のエラー処理
    if len(args) != 2 or not args[1].isdecimal() or len(args[1]) != 6 or args[1][0] == '0':
        return embed_err

    time = args[1]
    track_info = track.search(args[0]) # [track_name, track_number]

    if track_info is None:
        return embed_err

    return spreadsheet.set_record(ctx.author, time, track_info[0], track_info[1])


# 記録の表示
def show_record(ctx: commands.Context, args: list[str]) -> list[discord.Embed]:
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_r track_name` or `_r username` or `_r number`",
        color = err_color
    )

    embed_list = [embed_err]
    file = None
    
    if len(args) == 0:
        embed_list, file = spreadsheet.show_user_records(ctx.author)
    elif len(args) == 1:
        sub_list = ['1', '2', '3', '4', '5']
        track_info = track.search(args[0]) # [track, track_number]
        is_user_exist = ctx.guild is not None and ctx.guild.get_member_named(args[0]) is not None

        # 引数が数字, コース名, ユーザ名で処理を変える
        if args[0] in sub_list:
            sub_time = args[0] + '.000'
            embed_list = spreadsheet.show_sub_records(ctx.author, sub_time)
        elif track_info is not None:
            embed_list, file = spreadsheet.show_record(ctx.author, track_info[0], track_info[1])
        elif is_user_exist:
            embed_list, file = spreadsheet.show_user_records(ctx.guild.get_member_named(args[0]))

    return embed_list, file
    

# コースの記録の表示
def track_records(ctx: commands.Context, args: list[str]) -> discord.Embed:
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_t track_name`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err
    
    if ctx.guild is None:
        embed_err.title = "Not server"
        embed_err.description = "このコマンドはDMでは使用できません"
        return embed_err
    
    track_info = track.search(args[0]) # [track_name, track_number]
    if track_info is None:
        return embed_err

    # サーバーに所属するメンバーのIDリストを作成
    members_id_list = set(map(lambda m: str(m.id), ctx.guild.members))

    return spreadsheet.track_records(members_id_list, track_info[0], track_info[1])


def tier_time(ctx: commands.Context, args: list[str]) -> discord.Embed:
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_tt track_name`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err

    track_info = track.search(args[0]) # [track_name, track_number]
    if track_info is None:
        return embed_err
    
    return spreadsheet.show_tier_time(ctx.author, track_info[0], track_info[1])


# 記録の削除
def delete_record(ctx: commands.Context, args: list[str]) -> discord.Embed:
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_d track_name`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err
    
    track_info = track.search(args[0]) # [track_name, track_number]
    if track_info is None:
        return embed_err

    return spreadsheet.delete_record(ctx.author, track_info[0], track_info[1])


# 解説動画URLを送信
def send_video_url(args: list[str]) -> str:
    if len(args) != 1:
        return "Input error"
    
    track_info = track.search(args[0]) # [track_name, track_number]
    if track_info is None:
        return "No track"

    return spreadsheet.video_url(track_info[1])


def user_data() -> discord.Embed:
    return spreadsheet.user_data()


# WRの表示
def show_wr(args: list[str]) -> discord.Embed:
    embed = discord.Embed(
            color = 0x00ff00,
    )

    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_wr track_name`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err

    track_info = track.search(args[0]) # [track_name, track_number]

    if track_info is None:
        return embed_err

    return spreadsheet.show_wr(track_info[0], track_info[1])