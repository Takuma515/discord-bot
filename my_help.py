from discord.ext import commands
import discord


def my_help(bot: commands.AutoShardedBot) -> discord.Embed:
    embed = discord.Embed(title = "Command List")

    for command in bot.commands:
        if command.hidden:
            continue
        embed.add_field(
            name = command.name,
            value = f"> {command.description}",
            inline=False
        )
    return embed