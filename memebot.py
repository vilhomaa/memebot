import discord
import random
import praw
import requests
from discord.ext import commands
from itertools import islice
from itertools import cycle
import asyncio
import math
from datetime import date
import os
## Botti memejen postaamiseen discord channeliisi

#======================================================================================
# KONFIGURAATIOITA
#======================================================================================


## määrittää miten bottia voi kutsua discordissa
bot = commands.Bot(command_prefix = 'xd ', description = 'botti joka postaa meemejä')

## määrittää Tokenin, client id:n ja clientsecretin, nämä kaikki saa discordin api:stä
os.chdir("Z:\\python")
import login_details
TOKEN = login_details.TOKEN
clientid =login_details.clientid
clientsecret = login_details.clientsecret

## tässä kaikki subredditit josta botti voi hakea meemejä

subreddits = ['memes', 'dankmemes', 'meirl', 'wholesomememes', 'blackpeopletwitter', 'memeeconomy',
            'bee_irl', 'metal_me_irl', 'coaxedintoasnafu','195','shittyadviceanimals',
            'me_irl', '2meirl4meirl',  'comedycemetery', 'prequelmemes','terriblefacebookmemes',
            'HoldMyBeer', 'holdmycosmo', 'holdmyfeedingtube','CrappyDesign',
            'TrippinThroughTime', 'PerfectTiming', 'NoContextPics', 'CringePics']

## funktio siihen kauanko classic wowin release dateen oli aikaa, voi määrittää uusiksi
today = date.today()
kunnes_classic = str(27-int(today.strftime("%d")))+ " päivää classic wowiin"

# miltä kaikilta ajoilta memebot voi hakea redditistä
times = ['all', 'year', 'month', 'week', 'day', 'hour']
# mitä memebotin vaihtelevassa statuksessa voi lukea, vaihtaa näitä aina tasaisin väliajoin
status =  ['Quieres Memes?', "It's levio-SAAAH", 'Benjolöylyis', 'onks akel darra taas?',
            'LFG ULDMEN DUNGEN', 'All I want for xmas is Spens','muista tsekkaa jessen memet',
            kunnes_classic, 'Etsii memei']
msgs = cycle(status)

## kirjautuu redditin api:hin
reddit = praw.Reddit(client_id = clientid,client_secret = clientsecret ,user_agent=login_details.user_agent,
                    username = login_details.username,
                    password = login_details.password)


#======================================================================================
# ITSE BOTIN FUNKTIOITA, LUE ALHAALTA HELP MENUSTA MITÄ NE TEKEE TARKALLEEN
#======================================================================================

# funktio statuksen vaihtamiseen
async def change_status():
    while True:
        current_status = next(msgs)
        await bot.change_presence(activity=discord.Game(name = current_status))
        await asyncio.sleep(5)


# Funktio yhden random memen postaamiseen discordiin
async def randompost(ctx, n=1):
    for n in range(n):
        ajalta = random.choice(times)
        sreddit = random.choice(subreddits)
        j = int(math.sqrt(sum(1 for x in reddit.subreddit(sreddit).top(ajalta))))
        i = random.randint(0,j)
        submission = next(islice(reddit.subreddit(sreddit).top(ajalta),i,i+1),1)
        if isinstance(submission,int):
            await ctx.send('valinta out of bounds')
            continue
        tittel = submission.title
        urli = submission.url
        await ctx.send(f'Subredditiltä: {sreddit} \nAjalta: {ajalta} \nKuvan nimi: {tittel}\n{urli}')

# Launch functio memelle
@bot.event 
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')
    bot.loop.create_task(change_status())
    
## tietyn määrän ja memejen hakemiseen
@bot.command()
async def memespls(ctx, a: str, b: str, c: int):
    for submission in reddit.subreddit(random.choice(subreddits)).top(b, limit = c):
        await ctx.send(submission.url)

## postaa memen
@bot.command()
async def randommeme(ctx,n=1):
    await randompost(ctx,n)

@bot.command()
async def subredditit(ctx):
    await ctx.send(subreddits)

@bot.command()
async def statukset(ctx):
    await ctx.send(status)


@bot.command()
async def apua(ctx):
    await ctx.send("'Prefixi on 'xd', ja mahdolliset komennot ovat:\n" 
                    "----------------------------------------------\n"
                    'memespls [subreddit] [ajalta] [monta] -- komento lähettää sredditin top memet valitulta ajalta\n'
                    "        Esim: 'xd memespls dankmemes day 2'\n"
                    "----------------------------------------------\n"
                    "randommeme [luku jos haluat enemmän kuin yhden] --  lähettää random memen\n"
                    "        Esim 'xd randommeme 2'\n"
                    "----------------------------------------------\n"
                    "memetä   -- Aloittaa random memejen lähettämisen\n"
                    "lopeta   -- Lopettaa memettämisen\n"
                    "        Esim: 'xd memetä'  tai 'xd lopeta'\n"
                    "----------------------------------------------\n"
                    "subredditit  -- listaa subredditit\n"
                    "statukset -- listaa botin statukset (mitä se ns pelaa)\n"
                    "           Sano ladelle jos haluat lisäyksiä näihin listoihin\n")

## funktio jatkuvasti memejen postailuun 10 sek välein
@bot.event
async def on_message(message):
    
    if message.content.startswith('xd memetä'):
        postaa = True
        channel = message.channel
        await channel.send('Memetys alkaa')
        def check(message):
            return message.content == 'xd lopeta'
        
        while postaa:
            await randompost(channel, n = 1)
            try:
                await bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                continue
            else:
                await channel.send('Memetys tauolla')
                break
    await bot.process_commands(message)




bot.run(TOKEN)


