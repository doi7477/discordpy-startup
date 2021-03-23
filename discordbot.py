import discord
from discord.ext import tasks
#from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os
import random
import traceback
import time

token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()

#せとうぽ-要塞攻略室
YOUSAI_CHANNEL_ID = 713535093469347955
#せとうぽ-幹部用
KANBU_CHANNEL_ID = 605428683364106288
g_yousai_notice_flg = 1

#全体ヘルプ文
embed = discord.Embed(title="/せとうぽ",description="ヘルプを呼び出します",color=0x00ff00)
embed.add_field(name="/せとうぽ おみくじ",value="おみくじを引きます",inline=False)
embed.add_field(name="/せとうぽ ぜくの装備消去",value="ぜくしーをせくしーにします",inline=False)

#管理部用ヘルプ文
embed2 = discord.Embed(title="/せとうぽ 要塞通知オン",description="21時の要塞通知をオンにします",color=0x00ff00)
embed2.add_field(name="/せとうぽ 要塞通知オフ",value="21時の要塞通知をオフにします",inline=False)

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
    # 要塞通知フラグ定義
    global g_yousai_notice_flg
    
    # 通知オフなら処理しない
    if g_yousai_notice_flg == 0:
        return
        
    #現在時刻取得
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime('%H:%M')
        
    # 21:00に要塞通知を行う
    if now == '21:00': 
        channel = client.get_channel(YOUSAI_CHANNEL_ID)
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
        await channel.send('せとうぽくん起動しました\r\n要塞通知設定リセット：デフォルトはONです')
        #pass
    
@client.event
async def on_message(message):
    # 要塞通知フラグ定義
    global g_yousai_notice_flg
    global embed
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    # 幹部用チャンネルの場合#################################
    if message.channel.id == KANBU_CHANNEL_ID:
        # 管理部用ヘルプ
        if message.content == '/せとうぽ':
#            await message.channel.send('◆幹部用チャンネル専用\r\n'
#                                       '/せとうぽ 要塞通知オン　：21時の要塞通知をオンにする\r\n'
#                                       '/せとうぽ 要塞通知オフ　：21時の要塞通知をオフにする\r\n'
#                                       '◆全体チャンネル\r\n'
#                                       '/せとうぽ おみくじ　　　：おみくじをします')
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed2)
            return
        
        # 要塞通知ON設定
        if message.content == '/せとうぽ 要塞通知オン':
            if g_yousai_notice_flg == 1:
                await message.channel.send('すでに要塞通知設定はオンです')
            else:
                g_yousai_notice_flg = 1
                await message.channel.send('要塞通知をオンに設定しました')
            return

        # 要塞通知OFF設定
        if message.content == '/せとうぽ 要塞通知オフ':
            if g_yousai_notice_flg == 0:
                await message.channel.send('すでに要塞通知設定はオフです')
            else:
                g_yousai_notice_flg = 0
                await message.channel.send('要塞通知をオフに設定しました')
            return
    
    # 全チャンネルの場合#################################
    if message.content == '/せとうぽ':
        await message.channel.send('/せとうぽ おみくじ　　　：おみくじをします')
        return
    
    if message.content == '/せとうぽ ぜくの装備消去':
        await message.channel.send('Zexlia さんの 装備全て を消去しました')
        await message.channel.send('<:zeku:717319120642637904>\r\n<:hadaka:823868389285560320>')
        return
    
    if message.content == '/せとうぽ おみくじ':
        rand_result = random.randint(1,100)
        if rand_result < 10:
            await message.channel.send('大吉 です')
        elif rand_result < 30:
            await message.channel.send('中吉 です')
        elif rand_result < 50:
            await message.channel.send('吉 です')
        elif rand_result < 70:
            await message.channel.send('末吉 です')
        elif rand_result < 88:
            await message.channel.send('凶 です')
        elif rand_result < 98:
            await message.channel.send('大凶 です')
        else:
            await message.channel.send('あなたは占えませんでした')
        return
    
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')


#ループ処理実行
loop.start()
client.run(token)
#bot.run(token)
