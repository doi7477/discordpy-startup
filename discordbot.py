import discord
from discord.ext import tasks
#from discord.ext import commands
from datetime import datetime, timedelta, timezone
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

@tasks.loop(seconds=60)
async def loop():
    #現在時刻取得
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime('%H:%M')
    if now == '15:36': 
        channel = client.get_channel(751149121876000851)
        if channel is None:
            pass
        else:
            await channel.send('正解' + now)
    else:
        channel = client.get_channel(751149121876000851)
        if channel is None:
            pass
        else:
            await channel.send('ちゃいます' + now)
#    client.send_message(client.get_channel('751149121876000851'), 'hello')

#ループ処理実行
loop.start()
client.run(token)


#bot.run(token)
