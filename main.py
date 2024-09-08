import aiohttp
from bs4 import BeautifulSoup
import re
from twitchio.ext import commands

bot = commands.Bot(
    token='', #Access token
    client_id='',
    nick='',
    prefix='!',
    initial_channels=['']
)


async def get_steamid(profileurl: str):
    url = f'https://findsteamid.com/steamid/{profileurl}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            data = soup.find_all('span', class_='text-orange-400')
            steamid = data[2].text
            return steamid


async def get_mmr(player_id):
    url = f'https://tracklock.gg/players/{player_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            mmr = soup.find('span', class_='text-green-400')
            data = mmr.text.split(" ")
            result = f'current mmr is {
                data[0]}, {data[1].strip("(#)")}'
            if len(data) == 2:
                return result
            return result + f'{data[2]}'


async def get_player_id(steamid):
    url = f'https://tracklock.gg/search?q={steamid}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            mmr = soup.find(
                'a', class_='font-medium text-blue-400 hover:underline')
            player_id = re.findall(r'\d+', mmr['href'])[0]
            return player_id


@bot.command(name='mmr')
async def mmr_command(ctx, name: str):
    profile_url = name
    steam_id = await get_steamid(profile_url)
    player_id = await get_player_id(steam_id)
    mmr_info = await get_mmr(player_id)
    await ctx.send(mmr_info)

if __name__ == "__main__":
    bot.run()
