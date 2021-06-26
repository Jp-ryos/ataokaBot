import discord
from discord.ext import commands
import asyncio
import os
import traceback
import datetime
from datetime import timedelta

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def test_ping(ctx):
    await ctx.send('pong')

@bot.command()
async def helloworld(ctx):
    await ctx.send('HelloWorld. \n このボットはataoka.io#0531によって実装されました。コマンド一覧を参照する場合は  /command  と入力してください。 \n ソースコードを参照したい場合はこちらから飛んでください→https://github.com/Jp-ryos/ataokaBot')

@bot.command()
async def command(ctx):
    await ctx.send('> -----コマンド一覧-----\n- /test_ping 疎通確認を行うコマンドです ping-pong!!!。 \n- /rect 募集を行うコマンドです。\n サーバと同期できなくなるので何度もボタンを連打するのはお控えください。\n\t 例） /rect Apex 4 500 \n\t 　　 /rect [arg0: 募集要項] [arg1: 人数] [arg2: 募集する時間（秒）]')

@bot.command()
async def rect(ctx, about = "募集\n", cnt = 4, settime = 10.0):
    cnt, settime, now = int(cnt), float(settime * 60), datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    end = now + timedelta(0, settime, 0)
    reaction_member = [">>>"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中\n", value=None, inline=True)
    test.add_field(name=f"(募集開始：{now})\n", value=None, inline=True)
    test.add_field(name=f"(募集終了予定：{end.strftime('%Y/%m/%d %H:%M:%S')})\n", value=None, inline=True)
    msg = await ctx.send(embed=test)
    #投票の欄
    await msg.add_reaction('⏫')
    await msg.add_reaction('✖')

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⏫' or emoji == '✖'

    while len(reaction_member)-1 <= cnt:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('指定の募集人数に達しませんでした。再度募集をかけてください。')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⏫':
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)

                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="指定の募集人数が集まりました。",value='\n'.join(reaction_member), inline=True)
                    await ctx.send(embed=finish)

            elif str(reaction.emoji) == '✖':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)

bot.run(token)
