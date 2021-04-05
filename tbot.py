import os
from discord.ext import commands
import discord
import ccrawler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command('hei')
async def hei(ctx):
    response = f"Oh hai {ctx.message.author.mention}"
    await ctx.reply(response,
            mention_author=True,
            #file=discord.File(r'/data/data/com.termux/files/home/sel.py'),
            embed=discord.Embed(title="test embed",
                url="https://manga.bilibili.com/detail/mc29562?from=manga_index",
                description="this the descrription"))

@bot.command('test')
async def test(ctx, fa=None, fb=None):
    print(f'fa: {fa}, fb: {fb}')
    await ctx.reply(f"fa : {fa}, fb: {fb}")

@bot.command('get')
async def get(ctx, link, chanum=None):
    await ctx.reply('please be patient, as it downloading in the background')
    result = ccrawler.mdownload(link, chanum)

    await ctx.reply(result)

@bot.command('cc')
async def cc(ctx):
    for a in range(5):
        await ctx.reply(a)
# async def on_message(message):
    # we do not want the bot to reply to itself
#    if message.author.id == client.user.id:
#        return

#    if message.content.startswith('!hello'):
#        await message.reply('Hello!', mention_author=True)
#    if message.content.startswith('!hei'):
#        await message.reply('Oh hai', mention_author=True)

# client = MyClient()
bot.run(TOKEN)

