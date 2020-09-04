import discord
from discord.ext import tasks
#from discord.ext import commands
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = 751149121876000851
client = discord.Client()
#bot = commands.Bot(command_prefix='/')

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
    channel = client.get_channel(751149121876000851)
    if channel is None:
        pass
    else:
        await channel.send('test')
#    client.send_message(client.get_channel('751149121876000851'), 'hello')

#ループ処理実行
loop.start()
client.run(token)


#bot.run(token)
