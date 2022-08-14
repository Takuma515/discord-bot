import discord
import track
import spreadsheet

err_color = 0xff3333

# 記録の登録
def set_record(ctx, args):
    embed = discord.Embed(
            color = 0x00ff00,
    )

    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_s ttc 150123`",
        color = err_color
    )
    if len(args) != 2:
        return embed_err
    if not args[1].isdecimal():
        return embed_err
    if len(args[1]) != 6:
        return embed_err
    if args[1][0] == '0':
        return embed_err

    user = str(ctx.author)
    time = args[1]
    server = ctx.message.guild.name
    track_info = track.search(args[0])

    if track_info is None:
        return embed_err
    
    embed = spreadsheet.set_record(user, time, server, track_info[0], track_info[1]+2)

    return embed


# 記録の表示
def show_record(ctx, args):
    embed_list = []

    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_r ttc`",
        color = err_color
    )

    user = str(ctx.author)
    server = ctx.message.guild.name
    
    if len(args) == 0:
        embed_list = spreadsheet.show_all_records(user, server)
    elif len(args) == 1:
        track_info = track.search(args[0])

        if track_info is None:
            return [embed_err]
        
        embed_list = [spreadsheet.show_record(user, server, track_info[0], track_info[1]+2)]
    else:
        embed_list = [embed_err]

    return embed_list


# コースの記録の表示
def track_records(ctx, args):
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_t ttc`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err
    
    track_info = track.search(args[0])
    if track_info is None:
        return embed_err

    server = ctx.message.guild.name

    return spreadsheet.track_records(server, track_info[0], track_info[1]+2)


# 記録の削除
def delete_record(ctx, args):
    embed_err = discord.Embed(
        title = "Input Error",
        description = "**Ex.** `_d ttc`",
        color = err_color
    )

    if len(args) != 1:
        return embed_err
    
    track_info = track.search(args[0])
    if track_info is None:
        return embed_err
    
    user = str(ctx.author)
    server = ctx.message.guild.name

    return spreadsheet.delete_record(user, server, track_info[0], track_info[1]+2)


# 解説動画URLを送信
def send_video(ctx, args):
    if len(args) != 1:
        return "error"
    
    track_info = track.search(args[0])
    if track_info is None:
        return "No Track"

    return spreadsheet.video_url(track_info[1]+2)