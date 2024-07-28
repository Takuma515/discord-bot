import discord
from discord.ext import commands
import track_info
import models.sheet as sheet
from controllers.utils import calc_time_diff, format_time, get_thumbnail_url


color_error = 0xff3333
color_green = 0x00ff00


def show_user_data() -> discord.Embed:
    mmr_list = sheet.fetch_mmr_list()
    tier_name = ['Unrated', 'Iron', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Sapphire', \
		'Ruby', 'Diamond', 'Master', 'Grandmaster']
    tier_range = [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 17000, 10**5]
    user_num_list = [0] * 11

    # tierごとの人数をカウント
    for mmr in mmr_list[7:]:
        if mmr == '':
            user_num_list[0] += 1
            continue

        for j in range(len(tier_name)):
            min_mmr, max_mmr = tier_range[j], tier_range[j+1]

            if min_mmr <= int(mmr) < max_mmr:
                user_num_list[j+1] += 1
                break


    description = '\n'.join(f'{tier_name[i]}: {user_num_list[i]}' for i in range(len(user_num_list)))
    description += f'\nTotal: {sum(user_num_list)}'
    embed = discord.Embed(title = 'User Data', description = description)

    return embed