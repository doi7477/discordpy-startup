import discord
#from discord.ext import commands
from discord.ext import tasks
import os
import traceback

#bot = commands.Bot(command_prefix='/')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = 751149121876000851

#@bot.event
#async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)


#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

@tasks.loop(seconds=3)
async def loop():
#    channel = client.get_channel(CHANNEL_ID)
#    await channel.send('時間だよ')  
    client.send_message(client.get_channel('751149121876000851'), 'hello')

#ループ処理実行
loop.start()
client.run(token)


#bot.run(token)
