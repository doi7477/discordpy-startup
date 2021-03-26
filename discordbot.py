import os
import random
import traceback
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import tasks

#Discord設定
token = os.environ['DISCORD_BOT_TOKEN']
intents = discord.Intents.all()
client = discord.Client(intents=intents)
presence = discord.Game('モンスターハンターライズ')

#せとうぽ サーバID
SERVER_ID = 578209286639976448
#せとうぽ-雑談
ZATUDAN_CHANNEL_ID = 578209286639976452
#せとうぽ-要塞攻略室
YOUSAI_CHANNEL_ID = 713535093469347955
#せとうぽ-幹部用
KANBU_CHANNEL_ID = 605428683364106288

#どい動物園-雑談
DEBUG_CHANNEL_ID = 751149121876000851
#どい動物園 サーバーID
DEBUG_SERVER_ID = 751149121284603935

#要塞通知フラグ
g_yousai_notice_flg = 1

#全体ヘルプ文
embed_help = discord.Embed(title="**コマンドリスト一覧**",description="",color=0x4169E1)
embed_help.add_field(name="**/せとうぽ**",value="--> ヘルプを呼び出します",inline=False)
embed_help.add_field(name="**/せとうぽ おみくじ**",value="--> おみくじを引きます",inline=False)
embed_help.add_field(name="**/せとうぽ ぜくの装備消去**",value="--> ぜくしーをせくしーにします",inline=False)

#幹部用ヘルプ文
embed_kanbu_help = discord.Embed(title="**管部用コマンドリスト一覧**",description="",color=0x4169E1)
embed_kanbu_help.add_field(name="**/せとうぽ 要塞通知オン**",value="--> 21時の要塞通知をオンにします\r\n",inline=False)
embed_kanbu_help.add_field(name="**/せとうぽ 要塞通知オフ**",value="--> 21時の要塞通知をオフにします\r\n",inline=False)

#テストようこそ文
strtit = "ようこそ せとうぽへ"
intcol = 0x4169E1
strpng = "https://img.altema.jp/altema/uploads/2019/03/2019y03m07d_1405336875.png"
strtmp = "以下で自己紹介をお願いします\r\n"\
         " <#771510773549629480> \r\n"\
         "\r\n"\
         ":large_blue_diamond: 基本ルール :large_blue_diamond: \r\n"\
         "以下リンクをご確認ください\r\n"\
         "https://discord.com/channels/578209286639976448/581850951682359296/773011836970205204\r\n"\
         "\r\n"\
         ":large_blue_diamond: 要塞の小学生作戦について :large_blue_diamond: \r\n"\
         "以下リンクをご確認ください\r\n"\
         "https://discord.com/channels/578209286639976448/713535093469347955/823523614795104277\r\n"\
         "\r\n"\
         ":large_blue_diamond: せとうぽくんについて :large_blue_diamond: \r\n"\
         "以下コマンドでご確認ください\r\n/せとうぽ\r\n"\
         "\r\n"\
         "不明点は気軽に連絡ください\r\n"

embed_test = discord.Embed(title=strtit,description="",color=intcol)
embed_test.add_field(name=":sparkles:テストさん:sparkles:\r\nご参加ありがとうございます",value=strtmp,inline=False)
embed_test.set_thumbnail(url=strpng)

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
    print('せとうぽくん起動しました')

    #プレイ中更新
    await client.change_presence(activity=presence)
    
    #幹部用 起動通知
    channel = client.get_channel(KANBU_CHANNEL_ID)
    if channel is None:
        pass
    else:          
        #await channel.send('せとうぽくん起動しました\r\n要塞通知設定リセット：デフォルトはONです')
        pass

    #デバッグ 起動通知
    channel_ready = client.get_channel(DEBUG_CHANNEL_ID)
    if channel_ready is None:
        pass
    else:          
        #await channel_ready.send('せとうぽくん起動しました')
        pass

##################### 新規参加者の処理 #####################
@client.event
async def on_member_join(member):
        print('新規メンバー参加処理')
        global strtmp
        global strpng
        global strtit
        global intcol

        # 通知用チャンネル取得
        channel_join = client.get_channel(DEBUG_CHANNEL_ID)
        if channel_join is None:
            pass
        else:
            print(f'参加したサーバーID-->[{member.guild.id}]')
            if member.guild.id != DEBUG_SERVER_ID:
                print('別サーバーに入っているのでスキップ')
                return
                  
            embed_join = discord.Embed(title=strtit,description="",color=intcol)
            embed_join.add_field(name=f":sparkles:{member.name}さん:sparkles:\r\nご参加ありがとうございます",value=strtmp,inline=False)
            embed_join.set_thumbnail(url=strpng)
            await channel_join.send(embed=embed_join)
        return
         
##################### メッセージ受信時の処理 #####################
@client.event
async def on_message(message):
    
    global g_yousai_notice_flg
    global embed_help
    global embed_kanbu_help
    global embed_test
    
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    ##################### 幹部用チャンネル #####################
    if message.channel.id == KANBU_CHANNEL_ID:
        # 管理部用ヘルプ
        if message.content == '/せとうぽ':
            print('幹部用ヘルプ表示処理')
            await message.channel.send(embed=embed_help)
            await message.channel.send(embed=embed_kanbu_help)
            return
        
        # 要塞通知ON設定
        if message.content == '/せとうぽ 要塞通知オン':
            print('要塞通知ON設定処理')
            if g_yousai_notice_flg == 1:
                await message.channel.send('すでに要塞通知設定はオンです')
            else:
                g_yousai_notice_flg = 1
                await message.channel.send('要塞通知をオンに設定しました')
            return

        # 要塞通知OFF設定
        if message.content == '/せとうぽ 要塞通知オフ':
            print('要塞通知OFF設定処理')
            if g_yousai_notice_flg == 0:
                await message.channel.send('すでに要塞通知設定はオフです')
            else:
                g_yousai_notice_flg = 0
                await message.channel.send('要塞通知をオフに設定しました')
            return

    ##################### 全チャンネル #####################
    if message.content == '/せとうぽ':
        print('ヘルプ表示処理')
        await message.channel.send(embed=embed_help)
        return
    
    if message.content == '/せとうぽ ぜくの装備消去':
        print('せくの装備消去表示処理')
        await message.channel.send('Zexlia さんの 装備全て を消去しました')
        await message.channel.send('<:zeku:717319120642637904>\r\n<:hadaka:823868389285560320>')
        return
    
    if message.content == '/せとうぽ おみくじ':
        print('おみくじ処理')
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

    # テストコマンド
    if message.content == '/せとうぽ テスト':
        print('テストコマンド実行処理')
        await message.channel.send(embed=embed_test)
        return
        
#実行
loop.start()
client.run(token)
