import discord
from discord.ext import tasks
#from discord.ext import commands
from datetime import datetime, timedelta, timezone
import os
import random
import traceback
#import configparser

token = os.environ['DISCORD_BOT_TOKEN']
intents=discord.Intents.all()
client = discord.Client(intents=intents)
presence = discord.Game('モンスターハンターライズ')

#せとうぽ-雑談
ZATUDAN_CHANNEL_ID = 578209286639976452
#せとうぽ-要塞攻略室
YOUSAI_CHANNEL_ID = 713535093469347955
#せとうぽ-幹部用
KANBU_CHANNEL_ID = 605428683364106288
#どい動物園-雑談
DEBUG_CHANNEL_ID = 751149121876000851
#要塞通知フラグ
g_yousai_notice_flg = 1

#全体ヘルプ文
embed = discord.Embed(title="**コマンドリスト一覧**",description="",color=0x4169E1)
embed.add_field(name="**/せとうぽ**",value="--> ヘルプを呼び出します",inline=False)
embed.add_field(name="**/せとうぽ おみくじ**",value="--> おみくじを引きます",inline=False)
embed.add_field(name="**/せとうぽ ぜくの装備消去**",value="--> ぜくしーをせくしーにします",inline=False)

#幹部用ヘルプ文
embed2 = discord.Embed(title="**管部用コマンドリスト一覧**",description="",color=0x4169E1)
embed2.add_field(name="**/せとうぽ 要塞通知オン**",value="--> 21時の要塞通知をオンにします\r\n",inline=False)
embed2.add_field(name="**/せとうぽ 要塞通知オフ**",value="--> 21時の要塞通知をオフにします\r\n",inline=False)

#テストようこそ文
strtest = "どい丸"
strtmp = "以下で自己紹介をお願いします\r\n"\
         " <#771510773549629480> \r\n"
         "\r\n"\
         ":large_blue_diamond: 基本ルール :large_blue_diamond: \r\n"\
         "以下リンクをご確認ください\r\n"\
         "https://discord.com/channels/578209286639976448/581850951682359296/773011836970205204\r\n"\
         "\r\n"\
         ":large_blue_diamond: せとうぽくんについて :large_blue_diamond: \r\n"\
         "以下コマンドでご確認ください\r\n/せとうぽ\r\n"\
         "\r\n"\
         "不明点は気軽に連絡ください\r\n"
embed_t = discord.Embed(title="ようこそ せとうぽへ",description="",color=0x4169E1)
embed_t.add_field(name=f":sparkles:{strtest}さん:sparkles:\r\nご参加ありがとうございます",value=strtmp,inline=False)
embed_t.set_thumbnail(url="https://img.altema.jp/altema/uploads/2019/03/2019y03m07d_1405336875.png")

#config_ini = configparser.ConfigParser()
#config_ini_path = 'hoge.ini'
#if os.path.exists(config_ini_path):
#    config_ini.read(config_ini_path, encoding='utf-8')

##################### 要塞通知処理 #####################
@tasks.loop(seconds=60)
async def loop():
    
    # グローバル変数定義
    global g_yousai_notice_flg
    
    # 要塞通知オフなら処理しない
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
                
#####################　起動時の処理 #####################
@client.event
async def on_ready():                
    # メッセージ受信時に動作する処理
    print('せとうぽくん起動しました。')
    await client.change_presence(activity=presence)
    channel = client.get_channel(KANBU_CHANNEL_ID)
    if channel is None:
        pass
    else:          
        #await channel.send('せとうぽくん起動しました\r\n要塞通知設定リセット：デフォルトはONです')
        pass

    #デバッグ 起動確認
    channel2 = client.get_channel(DEBUG_CHANNEL_ID)
    if channel2 is None:
        pass
    else:          
        await channel2.send('せとうぽくん起動しました')

##################### 新規参加者の処理 #####################
@client.event
async def on_member_join(member):
         channel3 = client.get_channel(ZATUDAN_CHANNEL_ID)
         if channel3 is None:
                  pass
         else: 
                  #ようこそ文
                  strtmp = "以下で自己紹介をお願いします\r\n"\
                           " <#771510773549629480> \r\n"
                           "\r\n"\
                           ":large_blue_diamond: 基本ルール :large_blue_diamond: \r\n"\
                           "以下リンクをご確認ください\r\n"\
                           "https://discord.com/channels/578209286639976448/581850951682359296/773011836970205204\r\n"\
                           "\r\n"\
                           ":large_blue_diamond: せとうぽくんについて :large_blue_diamond: \r\n"\
                           "以下コマンドでご確認ください\r\n/せとうぽ\r\n"\
                           "\r\n"\
                           "不明点は気軽に連絡ください\r\n"
                  embed3 = discord.Embed(title="ようこそ せとうぽへ",description="",color=0x4169E1)
                  embed3.add_field(name=f"{member.author.name}さん!!!\r\nご参加ありがとうございます",value=strtmp,inline=False)
                  embed3.set_thumbnail(url="https://img.altema.jp/altema/uploads/2019/03/2019y03m07d_1405336875.png")
                  await channel3.send(embed=embed3)
         
##################### メッセージ受信時の処理 #####################
@client.event
async def on_message(message):
    
    # グローバル変数定義
    global g_yousai_notice_flg
    global embed
    global embed2
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    ##################### 幹部用チャンネル #####################
    if message.channel.id == KANBU_CHANNEL_ID:
        # 管理部用ヘルプ
        if message.content == '/せとうぽ':
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
    
    ##################### 全チャンネル #####################
    if message.content == '/せとうぽ':
        await message.channel.send(embed=embed)
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
    
    if message.content == '/せとうぽ テスト':
        await message.channel.send(embed=embed_t)
        return
    
#        var1 = config_ini['DEFAULT']['User']
#        await message.channel.send(var1)
#        return
    
#ループ処理実行
loop.start()
client.run(token)

#bot = commands.Bot(command_prefix='/')

#@bot.event
#async def on_command_error(ctx, error):
#    orig_error = getattr(error, "original", error)
#    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#    await ctx.send(error_msg)

#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

#bot.run(token)
