import discord
from discord.ext import tasks
#from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

#せとうぽ-要塞攻略室
CHANNEL_ID = 713535093469347955
KANBU_CHANNEL_ID = 605428683364106288
gfort_notice_flg = 1

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
    global gfort_notice_flg
    
    # 通知オフなら処理しない
    if gfort_notice_flg == 0:
        return
        
    #現在時刻取得
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime('%H:%M')
        
    # 21:00に要塞通知を行う
    if now == '21:00': 
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            pass
        else:          
            await channel.send('@everyone 要塞だよ！全員集合！！')
            #pass
                
@client.event
async def on_ready():                
    # メッセージ受信時に動作する処理
    print('せとうぽくん起動しました。')
    channel = client.get_channel(KANBU_CHANNEL_ID)
    if channel is None:
        pass
    else:          
        await channel.send('せとうぽくん起動しました。\r\n要塞通知設定リセット：デフォルトはONです')
        #pass
    
@client.event
async def on_message(message):
    global gfort_notice_flg
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    # 要塞通知ON設定
    if message.content == '/setup on':
        if gfort_notice_flg == 1:
            await message.channel.send('すでに要塞通知設定はONです')
        else:
            gfort_notice_flg = 1
            await message.channel.send('要塞通知をONに設定しました')

    # 要塞通知OFF設定
    if message.content == '/setup off':
        if gfort_notice_flg == 0:
            await message.channel.send('すでに要塞通知設定はOFFです')
        else:
            gfort_notice_flg = 0
            await message.channel.send('要塞通知をOFFに設定しました')
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')


#ループ処理実行
loop.start()
client.run(token)
#bot.run(token)
