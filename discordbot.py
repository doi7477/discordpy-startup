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
presence = discord.Game('Apex Legends')

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
         ":large_blue_diamond: 要塞の立ち回り方 :large_blue_diamond: \r\n"\
         "以下リンクをご確認ください\r\n"\
         "https://discord.com/channels/578209286639976448/713535093469347955/849246973202923531\r\n"\
         "\r\n"\
         ":large_blue_diamond: せとうぽくんについて :large_blue_diamond: \r\n"\
         "以下コマンドでご確認ください\r\n/せとうぽ\r\n"\
         "\r\n"\
         "不明点は気軽に連絡ください\r\n"

embed_test = discord.Embed(title=strtit,description="",color=intcol)
embed_test.add_field(name=":sparkles:テストさん:sparkles:\r\nご参加ありがとうございます",value=strtmp,inline=False)
embed_test.set_thumbnail(url=strpng)

#ゴールドアップル関連
ga_date = '2週目：2021年06月08日(火)10:00 ～ 06月15日(火)09:59'
ga_list = ['偉大なマグナス魂の玉交換券',
         '偉大なブラッディクイーン魂の玉交換券',
         '偉大なピエール魂の玉交換券',
         '金色刻印の印章交換券',
         '銀色刻印の印章交換券',
         '銅色刻印の印章交換券',
         '永遠の転生の炎交換券',
         '強力な転生の炎交換券',
         '嵐の成長の秘薬Lv145～150交換券',
         '嵐の成長の秘薬Lv140～145交換券',
         '嵐の成長の秘薬Lv130～140交換券',
         '嵐の成長の秘薬Lv120～130交換券',
         'スターフォース★+1高級確率強化クーポン(★18～19)交換券',
         'スターフォース★+1高級確率強化クーポン(★14～17)交換券',
         'スターフォース★+1確率強化クーポン(★18～19)交換券',
         'スターフォース★+1確率強化クーポン(★14～17)交換券',
         'ジュエルボックス(SS)交換券',
         'プレミアムミックスヘアカラークーポン交換券',
         'ダメージスキンカスタムスロット拡張券交換券',
         'パワフルなピエール魂の玉交換券',
         '俊敏なピエール魂の玉交換券',
         '聡明なピエール魂の玉交換券',
         '驚きのピエール魂の玉交換券',
         '派手なピエール魂の玉交換券',
         '強力なピエール魂の玉交換券',
         '光るピエール魂の玉交換券',
         '強靭なピエール魂の玉交換券',
         '階段スライド椅子交換券',
         'カフェ椅子交換券',
         'あたふたティータイムライディング交換券',
         '暁ダメージスキン交換券',
         'シルバーハート交換券',
         'Lv120～140武器解放の鍵(-40Lv)交換券',
         'Lv120～140防具解放の鍵(-40Lv)交換券',
         'Lv120～140武器解放の鍵(-20Lv)交換券',
         'Lv120～140防具解放の鍵(-20Lv)交換券',
         '嵐の成長の秘薬Lv100～120交換券',
         '不思議な武器魔石(レジェンダリー)交換券',
         '不思議な防具魔石(レジェンダリー)交換券',
         '不思議な武器魔石(ユニーク)交換券',
         '不思議な防具魔石(ユニーク)交換券',
         'スターフォース★+1高級確率強化クーポン(★10～13)交換券',
         'スターフォース★+1確率強化クーポン(★10～13)交換券',
         'スターフォース★+1確率強化クーポン(★0～9)交換券',
         'スターフォース★15強化70%クーポン交換券',
         'スターフォース★15強化50%クーポン交換券',
         'スターフォース★15強化30%クーポン交換券',
         'スターフォース★14強化70%クーポン交換券',
         'スターフォース★14強化50%クーポン交換券',
         'スターフォース★14強化30%クーポン交換券',
         'スターフォース★13強化70%クーポン交換券',
         'スターフォース★13強化50%クーポン交換券',
         'スターフォース★13強化30%クーポン交換券',
         'スターフォース★12強化100%クーポン交換券',
         'スターフォース★12強化70%クーポン交換券',
         'スターフォース★12強化50%クーポン交換券',
         'スターフォース★12強化30%クーポン交換券',
         'スターフォース★11強化100%クーポン交換券',
         'スターフォース★11強化70%クーポン交換券',
         'スターフォース★11強化50%クーポン交換券',
         'スターフォース★10強化100%クーポン交換券',
         'スターフォース★10強化70%クーポン交換券',
         'スターフォース★10強化50%クーポン交換券',
         'アクセサリースタフォ拡張石交換券',
         'パワフルなヴァンレオン魂の玉交換券',
         '俊敏なヴァンレオン魂の玉交換券',
         '聡明なヴァンレオン魂の玉交換券',
         '驚きのヴァンレオン魂の玉交換券',
         '派手なヴァンレオン魂の玉交換券',
         '強力なヴァンレオン魂の玉交換券',
         '光るヴァンレオン魂の玉交換券',
         '強靭なヴァンレオン魂の玉交換券',
         'パワフルなシグナス魂の玉交換券',
         '俊敏なシグナス魂の玉交換券',
         '聡明なシグナス魂の玉交換券',
         '驚きのシグナス魂の玉交換券',
         '派手なシグナス魂の玉交換券',
         '強力なシグナス魂の玉交換券',
         '光るシグナス魂の玉交換券',
         '強靭なシグナス魂の玉交換券',
         'パワフルなピンクビーン魂の玉交換券',
         '俊敏なピンクビーン魂の玉交換券',
         '聡明なピンクビーン魂の玉交換券',
         '驚きのピンクビーン魂の玉交換券',
         '派手なピンクビーン魂の玉交換券',
         '強力なピンクビーン魂の玉交換券',
         '光るピンクビーン魂の玉交換券',
         '強靭なピンクビーン魂の玉交換券',
         'ラッキーデイの書(7%)交換券',
         'ラッキーデイの書(5%)交換券',
         'セーフティーシールド交換券',
         'プロテクトシールド交換券',
         '潜在能力の書(エピック)50%交換券',
         '潜在能力の書(エピック)100%交換券',
         'ロイヤルヘアクーポン交換券',
         'ロイヤル整形クーポン交換券',
         'SP初期化の書交換券',
         'キャラクタースロット増加クーポン交換券',
         '自動戦闘チャージ券(1時間)交換券(高級)',
         '自動戦闘チャージ券(30分)交換券(高級)',
         '嵐の成長の秘薬Lv51～100交換券',
         '蛇鍋交換券(高級)',
         'エビのテンプラ交換券',
         'フルーツ生クリームケーキ交換券',
         'フルーツヨーグルト交換券',
         'グレープジュース交換券',
         'イエロー経験値アップクーポン交換券',
         'パワフルなジャクム魂の玉交換券',
         '俊敏なジャクム魂の玉交換券',
         '聡明なジャクム魂の玉交換券',
         '驚きのジャクム魂の玉交換券',
         '派手なジャクム魂の玉交換券',
         '強力なジャクム魂の玉交換券',
         '光るジャクム魂の玉交換券',
         '強靭なジャクム魂の玉交換券',
         '曜日ダンジョン掃討券',
         '自動戦闘チャージ券(1時間)交換券',
         '自動戦闘チャージ券(30分)交換券(中級)',
         '自動戦闘チャージ券(10分)交換券(高級)',
         'バフフリーザー交換券(高級)',
         'プレミアム生命の水(30日)交換券',
         'プレミアム生命の水(15日)交換券',
         '倉庫スロット拡張券交換券',
         'インベントリ拡張券交換券',
         '蛇鍋交換券',
         'オレンジ経験値アップクーポン交換券',
         'ハロウィンキャンディ交換券',
         'ハンバーガー交換券',
         'パープル経験値アップクーポンLv1交換券',
         'おでん(皿)交換券',
         'おでん(串)交換券',
         '転生の炎Lv120交換券',
         '120レベル無限HPポーション(2時間)交換券',
         '120レベル無限MPポーション(2時間)交換券',
         'Lv100～120武器解放の鍵(-10Lv)交換券',
         'Lv100～120防具解放の鍵(-10Lv)交換券',
         'Lv80～100武器解放の鍵(-20Lv)交換券',
         'Lv80～100防具解放の鍵(-20Lv)交換券',
         '不思議な武器魔石(エピック)交換券',
         '不思議な防具魔石(エピック)交換券',
         'バフフリーザー交換券(中級)',
         'レッドキューブ交換券',
         'ブラックキューブ交換券',
         'ひよこクッキー交換券',
         'ボンボンチョコレート交換券',
         'そば粉豆腐交換券',
         'イカのバター焼き交換券',
         'キャンディ箱交換券',
         '綿菓子交換券',
         'クロノスの卵交換券',
         'フィーバーバフチャージ券交換券',
         'レッド経験値アップクーポン交換券',
         '自動戦闘チャージ券(10分)交換券(中級)',
         'レインボーバルーンワールド拡声器(Lv30)交換券',
         '120レベル無限HPポーション(1時間)交換券',
         '120レベル無限MPポーション(1時間)交換券',
         'ココナッツジュース交換券',
         'クッキー交換券',
         '1杯のカフェラテ交換券',
         'フルーツキャンディ交換券',
         'ケーキ交換券',
         'ニンジンジュース交換券',
         '栗交換券',
         'スティックキャンディ交換券',
         'ギョーザ交換券',
         '不思議な武器魔石(レア)交換券',
         '不思議な防具魔石(レア)交換券',
         '100レベル無限HPポーション(2時間)交換券',
         '100レベル無限MPポーション(2時間)交換券',
         '装備ダンジョン入場券',
         'ネトのピラミッド入場券',
         '武陵道場入場券']
ga_weight = [0.01,
         0.02,
         0.02,
         0.06,
         0.1,
         0.13,
         0.07,
         0.1,
         0.06,
         0.06,
         0.07,
         0.09,
         0.07,
         0.12,
         0.08,
         0.12,
         0.08,
         0.06,
         0.16,
         0.09,
         0.09,
         0.09,
         0.09,
         0.09,
         0.09,
         0.09,
         0.09,
         0.4,
         0.4,
         0.35,
         0.05,
         0.1,
         0.04,
         0.04,
         0.06,
         0.06,
         0.06,
         0.05,
         0.05,
         0.08,
         0.08,
         0.15,
         0.17,
         0.2,
         0.14,
         0.17,
         0.19,
         0.15,
         0.17,
         0.19,
         0.16,
         0.2,
         0.19,
         0.17,
         0.19,
         0.2,
         0.2,
         0.18,
         0.19,
         0.2,
         0.18,
         0.19,
         0.2,
         0.15,
         0.12,
         0.12,
         0.12,
         0.12,
         0.12,
         0.11,
         0.11,
         0.12,
         0.12,
         0.12,
         0.12,
         0.12,
         0.12,
         0.11,
         0.11,
         0.12,
         0.18,
         0.19,
         0.19,
         0.19,
         0.19,
         0.18,
         0.18,
         0.19,
         0.39,
         0.42,
         0.34,
         0.34,
         0.18,
         0.16,
         0.52,
         0.52,
         0.29,
         0.52,
         0.47,
         0.47,
         0.6,
         0.53,
         0.55,
         0.55,
         0.55,
         0.55,
         0.53,
         0.27,
         0.27,
         0.27,
         0.27,
         0.27,
         0.21,
         0.21,
         0.22,
         0.65,
         0.94,
         0.94,
         0.94,
         0.97,
         0.64,
         1.16,
         1.16,
         1.17,
         1.04,
         1.04,
         1.04,
         1.04,
         1.04,
         1.16,
         1.16,
         0.88,
         0.52,
         0.52,
         0.17,
         0.17,
         0.19,
         0.19,
         0.24,
         0.24,
         2.65,
         2.76,
         2.74,
         2.45,
         2.45,
         2.45,
         2.45,
         2.45,
         2.45,
         1.61,
         2.46,
         2.46,
         2.54,
         2.76,
         1.06,
         1.06,
         1.49,
         1.49,
         1.51,
         1.49,
         1.51,
         1.48,
         1.48,
         1.48,
         1.49,
         0.7,
         0.7,
         1.07,
         1.07,
         1.68,
         1.68,
         1.68]

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
        await channel_ready.send('せとうぽくん起動しました')
        #pass

##################### 新規参加者の処理 #####################
@client.event
async def on_member_join(member):
        print('新規メンバー参加処理')
        global strtmp
        global strpng
        global strtit
        global intcol

        # 通知用チャンネル取得
        channel_join = client.get_channel(ZATUDAN_CHANNEL_ID)
        if channel_join is None:
            pass
        else:
            print(f'参加したサーバーID-->[{member.guild.id}]')
            if member.guild.id != SERVER_ID:
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

    # ゴールドアップルコマンド
    if message.content == '/せとうぽ GA':
        print('GAコマンド実行処理')
        ga_result = random.choice(ga_list, weights=ga_weight, k=11)
        ga_result_str = ga_date+ '\r\n' + ga_result
        await message.channel.send(ga_result_str)
        return

    # テストコマンド
    if message.content == '/せとうぽ テスト':
        print('テストコマンド実行処理')
        await message.channel.send(embed=embed_test)
        return


#実行
loop.start()
client.run(token)
