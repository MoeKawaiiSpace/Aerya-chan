# Project Name: Aerya
# Last Modified: Sep 27, 2020
# Author: Aki 
# ------------------------

# Import necessary library
import discord
import re
import argparse
import shlex
from discord.ext.commands.errors import BadArgument
import humanfriendly
import random
import asyncio
import datetime
from discord.ext import commands
from typing import Optional
import psutil
import platform
from discord.ext.commands import PartialEmojiConverter
from discord.ext.commands import MemberConverter
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands import Cog
from discord.ext.commands.cooldowns import BucketType
from jikanpy import  Jikan

class ArgParse(argparse.ArgumentParser):
    def error(self, message):
        raise commands.BadArgument(message)

# Cooldown 60 secs per 6xp
class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    # XP and Vallis increase function
    @Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if not retry_after:
            await self.bot.pg_con.execute("UPDATE profile_ext SET xpg = xpg+6 WHERE user_id = $1",message.author.id)    
            xpg = await self.bot.pg_con.fetchrow("SELECT xpg FROM profile_ext WHERE user_id = $1",message.author.id)
            if xpg['xpg'] % 150 == 0:
                await self.bot.pg_con.execute("UPDATE profile_ext SET bal = bal + 1500 WHERE user_id = $1",message.author.id)
                await message.channel.send(f"{message.author.mention} has been awarded 1500 Vallis! Keep being active on Discord :partying_face:" )
   
    # Shop command
    @commands.command()
    async def shop(self,ctx):
        items = await self.bot.pg_con.fetch("SELECT * FROM shop")
        embed = discord.Embed(title = 'Badges Shop',description='Use a!buy command to buy badges from the shop.',color = discord.Color(random.randint( 0, 16777216)))
       
        n = 1
        for i in items:
            name = i['name']
            id = i['id']
            cost = i['money']
            embed.add_field(name=f'{n}) {name}',value = f'{id} ``Cost: {cost}``')
       
           
            n+=1
        await ctx.send(embed = embed)   
    
    # Buy command
    @commands.command()
    async def buy(self,ctx,*,name):
        names = await self.bot.pg_con.fetch("SELECT * FROM shop")
        
        for i in names:
            if name.lower() == i['name'].lower():
                user = await self.bot.pg_con.fetch("SELECT * FROM profile_ext WHERE user_id = $1",ctx.author.id)
                cost = i['money']
                if user[0]['bal'] >= cost:
                    list = user[0]['badges']
                    list.append(i['id'])
                    left = user[0]['bal'] - cost
                    await self.bot.pg_con.execute("UPDATE profile_ext SET bal = $1 WHERE user_id = $2",left,ctx.author.id)
                    await self.bot.pg_con.execute("UPDATE profile_ext SET badges = $1::TEXT[] WHERE user_id = $2",list,ctx.author.id)
                    await ctx.send("Bought item :thumbsup:")
                else:
                    await ctx.send("Looks like you dont have enough money to buy this item :(")

    # Avatar command
    @commands.command()
    async def avatar(self,ctx,server=None):
        if not server:
            url = ctx.author.avatar_url
            embed = discord.Embed(color = discord.Color(random.randint( 0, 16777216))).set_image(url = url)
            await ctx.send(embed = embed)           
        else:
            if server.lower() == "server":
                url = ctx.guild.icon_url
                embed = discord.Embed(color = discord.Color(random.randint( 0, 16777216))).set_image(url = url)
                await ctx.send(embed = embed)  
            else:
                if await MemberConverter().convert(ctx,server):
                    srvr = await MemberConverter().convert(ctx,server)
                    url = srvr.avatar_url
                    embed = discord.Embed(color = discord.Color(random.randint( 0, 16777216))).set_image(url = url)
                    await ctx.send(embed = embed)                       
    
    # XPGLB command
    @commands.command()
    async def xpglb(self,ctx):
        info = await self.bot.pg_con.fetch("SELECT user_id, xpg FROM profile_ext ORDER BY xpg DESC LIMIT 10")
        embed = discord.Embed(color = discord.Color(random.randint( 0, 16777216)),title = "Global XP Rank")
        n2 = 1
        for i in info:
            m = self.bot.get_user(i['user_id'])
            embed.add_field(name="\u200b", value = f"{n2}) {m.display_name} - XP:``{i['xpg']}``",inline = False)
            n2 +=1
        await ctx.send(embed = embed)

    # BALGLB command
    @commands.command()
    async def balglb(self,ctx):
        info = await self.bot.pg_con.fetch("SELECT user_id, bal FROM profile_ext ORDER BY bal DESC LIMIT 10")
        embed = discord.Embed(color = discord.Color(random.randint( 0, 16777216)),title = "Global Vallis Rank")
        n2 = 1
        for i in info:
            m = self.bot.get_user(i['user_id'])
            embed.add_field(name="\u200b", value = f"{n2}) {m.display_name} - Vallis:``{i['bal']}``",inline = False)
            n2 +=1
        await ctx.send(embed = embed)
       
    # Check balance command
    @commands.command(aliases = ['bal'])
    async def balance(self,ctx,member:discord.Member=None,amount:int=None):
        if member == None:
            bal = await self.bot.pg_con.fetch("SELECT bal FROM profile_ext WHERE user_id = $1",ctx.author.id)
            await ctx.send(f"Your balance: ``{bal[0]['bal']}`` Vallis")
        elif member != None and amount != None:
            bal = await self.bot.pg_con.fetch("SELECT bal FROM profile_ext WHERE user_id = $1",ctx.author.id)
            if amount <= bal[0]['bal']: 
                await self.bot.pg_con.execute("UPDATE profile_ext SET bal = bal + $1 WHERE user_id = $2",amount,member.id)  
                rest = bal[0]['bal'] - amount
                await self.bot.pg_con.execute("UPDATE profile_ext SET bal = $1 WHERE user_id = $2",rest,ctx.author.id)
                await ctx.send(f"Transferred ``{amount}`` Vallis to {member.display_name}")
            else:
                await ctx.send("You don't have that much amount to transfer")

    # Shop set command
    @commands.command()
    async def shop_set(self,ctx,*,args):
        if ctx.author.id == 523685858658746397:
                parser = ArgParse()
                parser.add_argument('--name', type=str, nargs='+')
                parser.add_argument('--emoji', type=str)
                parser.add_argument('--cost', type=int)
                args = parser.parse_args(shlex.split(args))
                name = args.name # Will be name
                emoji = args.emoji # Will be emoji
                cost = args.cost
                
                if len(str(emoji)) > 1:
                    return await ctx.send("You have entered an animated or custom emoji. Try again")
                else:
                    n = ' '.join(x for x in name)
                    await self.bot.pg_con.execute("INSERT INTO shop(name,id,money) VALUES($1,$2,$3)",n,emoji,cost)
                    await ctx.send("Item added to shop :thumbsup:")    
        else:
            await ctx.send("Sorry, you are not eligible to use this command")                     

    #Stats command
    @commands.command()
    async def stats(self,ctx):
        voicechannels=[]
        textchannels=[]

        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                voicechannels.append(channel)

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                textchannels.append(channel)


        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        totalcpu=psutil.cpu_count(logical=True)
        totalservers = len(self.bot.guilds)
        totalusers = len(self.bot.users)
        cpufreq = psutil.cpu_freq()
        cpufrq=(f"{cpufreq.max:.2f}Mhz")
        net_io = psutil.net_io_counters()
        cpumodel = (platform.processor())
        cpu_usage=(psutil.cpu_percent())
        ram_usage=(psutil.virtual_memory()[2])
        current_time = datetime.datetime.utcnow()
        uptime_inseconds = round((current_time - self.bot.start_time).total_seconds())
        days = int(uptime_inseconds/86400)
        s = int(uptime_inseconds%86400)
        hours = int(s/3600) 
        s = int(s % 3600)
        minutes = int(s/60) 
        seconds = int(s % 60)
        embed = discord.Embed(
            title = "Bot Info",
            color = discord.Color(random.randint( 0, 16777216))
        )
        embed.add_field(name="Bot ID" , value=f"641780922445856768")
        embed.add_field(name="\u200b" , value=f"\u200b")
        embed.add_field(name="Bot Owner" , value="**Aki#1706** (ID: 523685858658746397)")

       

        embed.add_field(name = "CPU Usage", value = f"{cpu_usage}%")
        embed.add_field(name ="\u200b" , value=f"\u200b")
        embed.add_field(name = "Ram Usage", value = f"{ram_usage}%")
        

        
        embed.add_field(name ="Serving in", value = f"**{totalservers}** Servers")
        embed.add_field(name ="\u200b" , value=f"\u200b")
        embed.add_field(name ="Serving for" , value=f"**{totalusers}** Users")

        embed.add_field(name ="Uptime" , value=f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ",inline=False)



        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        await ctx.send(embed = embed)

    # Help + Rep command
    @commands.command()
    async def help(self,ctx):
        await ctx.send("**Looking for my command list senpai? Click here:** https://aerya.moe \nAnd here is my Sportsbook FULL GUIDE if you are looking for it: https://gist.github.com/Aki176/d1709558004f3c779af4f5f93b7eaf58")    
    # Vote command
    @commands.command()
    async def vote(self,ctx):
        await ctx.send("I really appreciate it if you give me a vote on those website!: https://disbots.gg/bot/641780922445856768")

    @commands.command(aliases = ['rep'])
    @commands.guild_only()
    @commands.cooldown(1,86400,BucketType.user)
    async def reputation(self,ctx, member:discord.Member=None):
        if member == None:
            await ctx.send("Please specify a member")

        elif member.id == ctx.author.id:    
            await ctx.send("You cannot rep yourself")
        else:
            await self.bot.pg_con.execute("UPDATE profile_ext SET reputation = reputation+1 WHERE user_id = $1 ",member.id)    
            await ctx.send(f"Awarded {member.display_name} with one reputation point")
    @reputation.error
    async def rps_error(self,ctx, e):
            if isinstance(e, commands.CommandOnCooldown):
                wait = discord.Embed(description = f"Hey there! Wait for {int(e.retry_after/3600)} hrs until you can use this command agn again :clock:  ")
                await ctx.send(embed = wait)
            else:
                raise       
    @commands.command(aliases=['daily'])
    @commands.cooldown(1,86400,BucketType.user) 
    async def login(self,ctx):
        await self.bot.pg_con.execute("UPDATE profile_ext SET bal = bal + 1000 WHERE user_id = $1",ctx.author.id)
        await ctx.send("Baka! B-b-but here is your ``1000`` Vallis!!")
    @reputation.error
    async def login_error(self,ctx, e):
            if isinstance(e, commands.CommandOnCooldown):
                wait = discord.Embed(description = f"Hey there! Wait for {int(e.retry_after/3600)} hrs until you can use this command again :clock:  ")
                await ctx.send(embed = wait)
            else:
                raise  

    # Profile command  
    @commands.command()
    @commands.guild_only()
    async def profile(self,ctx,member:Optional[discord.Member]):
        if member:
            info = await self.bot.pg_con.fetch("SELECT * FROM profiles WHERE user_id = $1 AND guild_id = $2",member.id,ctx.guild.id)
            if info:
                embed = discord.Embed(title = "Member Profile",color = discord.Color(random.randint(0,16777216)))
                info2 = await self.bot.pg_con.fetch("SELECT * FROM profile_ext WHERE user_id = $1",member.id)            
                embed.description = info2[0]['description']
                embed.add_field(name = "Name", value=member.display_name, inline=True)
                embed.add_field(name = "Member ID",value = member.id, inline=True)
                embed.add_field(name = "Birthday",value = info2[0]['birthday'], inline=True)
                embed.add_field(name = "Gender",value = info2[0]['gender'], inline=True)
                embed.add_field(name = "Waifus/Husbando",value = info2[0]['waifus'], inline=True)
                embed.add_field(name = "XP Global", value = info2[0]['xpg'], inline=True)
                embed.add_field(name = "Vallis",value = info2[0]['bal'], inline=True)
                embed.add_field(name = "Reputation",value  = info2[0]['reputation'], inline=True)
                embed.add_field(name = "Badges", value = info2[0]['badges'], inline=True)
            else:               
                await ctx.send("Oops, looks like the member has not been active in the server. Try again later...")    
        else:
            embed = discord.Embed(title = "Member Profile",color = discord.Color(random.randint(0,16777216)))
            info = await self.bot.pg_con.fetch("SELECT * FROM profiles WHERE user_id = $1 AND guild_id = $2",ctx.author.id,ctx.guild.id)
            if info:
                info2 = await self.bot.pg_con.fetch("SELECT * FROM profile_ext WHERE user_id = $1",ctx.author.id)            
                embed.description = info2[0]['description']
                embed.add_field(name = "Name", value=ctx.author.display_name, inline=True)               
                embed.add_field(name = "Member ID",value = ctx.author.id, inline=True)
                embed.add_field(name = "Birthday",value = info2[0]['birthday'], inline=True)
                embed.add_field(name = "Gender",value = info2[0]['gender'], inline=True)
                embed.add_field(name = "Waifus/Husbando",value = info2[0]['waifus'], inline=True)
                embed.add_field(name = "XP Global", value = info2[0]['xpg'], inline=True)
                embed.add_field(name = "Vallis",value = info2[0]['bal'], inline=True)
                embed.add_field(name = "Reputation",value  = info2[0]['reputation'], inline=True)
                embed.add_field(name = "Badges", value = info2[0]['badges'], inline=True)
        await ctx.send(embed = embed)
    


    # Set description command
    @commands.command()
    async def setdesc(self,ctx,*,desc:str):
        await self.bot.pg_con.execute("UPDATE profile_ext SET description = $1 WHERE user_id = $2",desc,ctx.author.id)
        await ctx.send("Description updated :thumbsup:")

    # Set birthday command
    @commands.command()
    async def setbday(self,ctx,*,bday:str):
        await self.bot.pg_con.execute("UPDATE profile_ext SET birthday = $1 WHERE user_id = $2",bday,ctx.author.id)  
        await ctx.send("Birthday updated :thumbsup:")

    # Set gender command
    @commands.command()
    async def setgender(self,ctx,*,gender:str):
        await self.bot.pg_con.execute("UPDATE profile_ext SET gender = $1 WHERE user_id = $2",gender,ctx.author.id)
        await ctx.send("Gender updated :thumbsup:")

    # Hack Vallis command
    @commands.command()
    async def hackbal(self,ctx,*,vallis:int):
        l = [523685858658746397]
        if ctx.author.id in l:
            await self.bot.pg_con.execute("UPDATE profile_ext SET bal = $1 WHERE user_id = $2",vallis,ctx.author.id)
            await ctx.send("Hack Vallis succeed! Baka cheater!")
        else:
            await ctx.send("Sorry, you are not eligible to use this command")

    # Hack badge command
    @commands.command()
    async def hackbadge(self,ctx,*,name):
        l = [523685858658746397]
        if ctx.author.id in l:
            names = await self.bot.pg_con.fetch("SELECT * FROM shop")
            for i in names:
                if name.lower() == i['name'].lower():
                    await self.bot.pg_con.execute("UPDATE profile_ext SET badges = $1::TEXT[] WHERE user_id = $2",list,ctx.author.id)
                    await ctx.send("Hack Badge succeed! Baka cheater!")
        else:
            await ctx.send("Sorry, you are not eligible to use this command")

    # Marriage command
    @commands.command()
    async def marriage(self,ctx,member:discord.Member):
        chk=await self.bot.pg_con.fetchrow("SELECT waifus FROM profile_ext WHERE user_id = $1 ",ctx.author.id)
        
        if chk['waifus'] == member.display_name:
            await ctx.send("You're already married to this member")

        else:    
            if not member:
                await ctx.send("Please specify a member to marry")      
            else:
                await ctx.send(f"{member.mention} {ctx.author.display_name}  wants to marry you. Do you accept(send 'accept' if yes):love_letter:")
                def check(m):
                    return m.author == member and m.content == 'accept'
                try:    
                    confirm = await self.bot.wait_for('message', check=check, timeout = 600)
                except asyncio.TimeoutError:
                    await ctx.send("The member took too long to respond. Try again...")
                else:
                    if confirm:
                        await self.bot.pg_con.execute("UPDATE profile_ext SET waifus = $1 WHERE user_id = $2 ",member.display_name,ctx.author.id) 
                        await self.bot.pg_con.execute("UPDATE profile_ext SET waifus = $1 WHERE user_id = $2 ",ctx.author.display_name,member.id)      
                        await ctx.send(f":heart: Yaay! {ctx.author.mention} married {member.mention}!! :partying_face: :partying_face:  ")
    
    # Search Anime command
    @commands.command()    
    async def anime(self,ctx,*,name):
        jikan = Jikan()
        a = jikan.search('anime',str(name))
        title = a['results'][0]['title']
        img_url = a['results'][0]['image_url']
        desc = a['results'][0]['synopsis']
        score = a['results'][0]['score']    
        rated = a['results'][0]['rated']
        url = a['results'][0]['url']
        embed = discord.Embed(title = title,description = desc,color =  discord.Color(random.randint(0,16777216)))
        embed.set_thumbnail(url = img_url)
        embed.add_field(name = 'Score', value = score)
        embed.add_field(name = 'Rated', value = rated)
        embed.add_field(name = 'URL', value = url,inline=False)
        embed.set_footer(text= "Not the result you were lookin for?....Enter the correct name next time and check if its anime")
        await ctx.send(embed = embed)     

    # Match bet module
    @commands.command()   
    async def match_bet(self,ctx):
        await ctx.send("Hi please join our and follow THIS channel to get sportsbook updates on your server. Thankyou! :grin: \nhttps://discord.gg/CVhk828 ")           
    
    # Set details bet slip command
    @commands.command()
    async def set_details(self,ctx,*,args):
        l = [523685858658746397]
        if ctx.author.id in l:
            parser = ArgParse()
            parser.add_argument('--slip', type=str)
            parser.add_argument('--date', type=str,nargs = '+')
            parser.add_argument('--game', type=str,nargs = '+')
            parser.add_argument('--event', type=str,nargs = '+')
            parser.add_argument('--match', type=str,nargs='+')
            parser.add_argument('--bet_on', type=str,nargs='+')
            parser.add_argument('--status', type=str,nargs='+')
            
            args = parser.parse_args(shlex.split(args))
            slip = args.slip
            date = args.date
            game = args.game
            event = args.event
            match = args.match
            bet_on = args.bet_on
            status = args.status
    
            embed = discord.Embed(title = f"{slip}",color =discord.Color(random.randint(0,16777216)))
            embed.description = f"**Date:** {' '.join(x for x in date)} \n**Game:** {' '.join(x for x in game)} \n**Event:** {' '.join(x for x in event)} \n**Match:** {' '.join(x for x in  match)} \n**Bet on:** {' '.join(x for x in bet_on)} \n**Percentage:** Will be displayed soon! \n**Odds:** ?/? \n**Status:** {' '.join(x for x in status)}"
            
            def check(m):
                return m.author == ctx.author
            await ctx.send(embed = embed)    
            await ctx.send("Here is the how the embed looks. Proceed?(answer with yes or no)")
            resp = await self.bot.wait_for('message',timeout = 60, check = check)
            if resp.content.lower() == 'yes':
                channel = self.bot.get_channel(758508639966724126)
                await ctx.send("Sending the embed...")
                msg = await channel.send(embed = embed)
                await msg.publish()
                await self.bot.pg_con.execute("INSERT INTO matchbet(slip_no,status,msg_id) VALUES($1,'on',$2)",slip,msg.id)
        else:
            await ctx.send("Sorry, you are not eligible to use this command")

    # Bet command
    @commands.command()
    async def bet(self,ctx,slip,choice,amount:int):
        chek = await self.bot.pg_con.fetchrow("SELECT * FROM matchbet_data WHERE user_id = $1 AND slip_no = $2",ctx.author.id,slip)
     
        if not chek:
            if amount >= 300:
                user = await self.bot.pg_con.fetchrow("SELECT * FROM profile_ext WHERE user_id = $1",ctx.author.id)
                if user['bal']>= 300:
                    check = await self.bot.pg_con.fetchrow("SELECT status FROM matchbet WHERE slip_no = $1",slip)
                    if check:
                        if check['status'] == 'on':
                            amt = user['bal'] - amount
                            await self.bot.pg_con.execute("UPDATE profile_ext SET bal = $1 WHERE user_id = $2",amt,ctx.author.id)
                            await self.bot.pg_con.execute("INSERT INTO matchbet_data(user_id,slip_no,amount,choice) VALUES($1,$2,$3,$4)",ctx.author.id,slip,amount,choice.lower())
                            await ctx.send("Registered :thumbsup:")
                        else:
                            await ctx.send("Sorry, this slip have been closed")
                    else:
                        await ctx.send("Hmm, looks like you have entered an invalid slip number") 
                else:
                    await ctx.send("You don't have enough money :(")       
            else:
                await ctx.send("The smallest amount to bet is 300 Vallis")          
        else:  
            await ctx.send("Hmm, looks like you've already registered")      

    # Stop the bet slip
    @commands.command()
    async def stop_bet(self,ctx,slip_no,*,odds):
        l = [523685858658746397]
        if ctx.author.id in l:
            await self.bot.pg_con.execute("UPDATE matchbet SET status = 'off' WHERE slip_no = $1",slip_no)
            left = await self.bot.pg_con.fetch("SELECT * FROM matchbet_data WHERE choice = 'left'")
            right = await self.bot.pg_con.fetch("SELECT * FROM matchbet_data WHERE choice = 'right'")
            left_per = (len(left)/(len(left)+len(right)))*100
            right_per = (len(right)/(len(right)+len(left)))*100
            id = await self.bot.pg_con.fetchrow("SELECT msg_id FROM matchbet WHERE slip_no = $1",slip_no)
            channel = self.bot.get_channel(758508639966724126)
            msg = await channel.fetch_message(id['msg_id'])
            desc = msg.embeds[0].description.replace('On','Off',1).replace('Will be displayed soon!',f'{left_per}%/{right_per}%',1).replace('?/?',str(odds),1)
            embed = discord.Embed(title = msg.embeds[0].title,color = msg.embeds[0].color,description = desc )       
            await msg.edit(embed = embed)
            await ctx.send(f"Registrations closed for slip {slip_no} :thumbsup:")
        else:
            await ctx.send("Sorry, you are not eligible to use this command")                
    
    # Declare winner
    @commands.command()
    async def declare_winner(self,ctx,slip_no,choice,multiplier):
        l = [523685858658746397]
        if ctx.author.id in l:
            winners = await self.bot.pg_con.fetch("SELECT * FROM matchbet_data WHERE slip_no = $1 AND choice = $2",slip_no,choice)
            for i in winners:
                credit = float(multiplier) * i['amount']
                await self.bot.pg_con.execute("UPDATE profile_ext SET bal = (bal + $1) WHERE user_id = $2",credit,i['user_id'])
            id = await self.bot.pg_con.fetchrow("SELECT msg_id FROM matchbet WHERE slip_no = $1",slip_no)
            channel = self.bot.get_channel(758508639966724126)
            msg = await channel.fetch_message(id['msg_id'])
            desc = msg.embeds[0].description.replace('Off','Ended',1)
            embed = discord.Embed(title = msg.embeds[0].title,color = msg.embeds[0].color,description = desc )       
            await msg.edit(embed = embed)       
            await self.bot.pg_con.execute("DELETE FROM matchbet_data WHERE slip_no = $1",slip_no)
      
            await self.bot.pg_con.execute("DELETE FROM matchbet WHERE slip_no = $1",slip_no)
            await ctx.send("Done :thumbsup:")
        else:
            await ctx.send("Sorry, you are not eligible to use this command")

    # Bet list 
    @commands.command()
    async def bet_list(self,ctx):
        data = await self.bot.pg_con.fetch("SELECT * FROM matchbet_data WHERE user_id = $1",ctx.author.id)
        if not data:
            await ctx.send("No records found")
        else:
            embed = discord.Embed(title = "Your Bet Slip List", color =discord.Color(random.randint(0,16777216)))
            x = 1
            n = 0
            for i in data:
                embed.add_field(name = f"{x}. Slip no",value = data[n]['slip_no'])
                embed.add_field(name = "Amount",value = data[n]['amount'])
                embed.add_field(name = "Choice",value = data[n]['choice'])
                x+=1
                n+=1
            await ctx.send(embed=embed)    

def setup(bot):
    bot.add_cog(Fun(bot))        
