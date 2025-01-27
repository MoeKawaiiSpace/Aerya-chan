# Project Name: Aerya
# Last Modified: Sep 27, 2020
# Author: Aki 
# ------------------------

# Import necessary library
import discord
import random
import datetime
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    # Server info
    @commands.command(aliases = ['sinfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        allMembers = len(ctx.guild.members)
        offline = len([a for a in ctx.guild.members if a.status == discord.Status.invisible])
        online = allMembers - offline
        botUsers = len([a for a in ctx.guild.members if a.bot])
        netUsers = allMembers - botUsers
        servericon = ctx.guild.icon_url
        emojis = len(ctx.guild.emojis)
        verification = ctx.guild.verification_level
        server_passed = (ctx.message.created_at - ctx.guild.created_at).days
        server_created_at = "Created on {}\nThat's {} days ago!".format(ctx.guild.created_at.strftime('%d %b %Y'), server_passed)

        TextChannelNumber = 0
        VoiceChannelNumber = 0
        Categories = 0

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                TextChannelNumber+=1

            elif isinstance(channel, discord.VoiceChannel):
                VoiceChannelNumber+=1

            else:
                Categories += 1

        boost_status=None

        if not ctx.guild.premium_subscription_count:
            boost_status="0"

        else:
            boost_status=f"{ctx.guild.premium_subscription_count}"

        Roles = 0
        guildroles = ", ".join(role.mention for role in ctx.guild.roles[1:])

        

        embed = discord.Embed(title="Server Information", color = discord.Color(random.randint( 0, 16777216)))
        embed.set_author(name=ctx.guild.name, icon_url=servericon)
        embed.add_field(name="Server Owner", value=ctx.guild.owner)
        embed.add_field(name="Server Region", value=ctx.guild.region)
        embed.add_field(name="Server Boosters", value=boost_status)
        embed.add_field(name="Channel Category", value=Categories)
        embed.add_field(name="Text Channels", value=TextChannelNumber)
        embed.add_field(name="Voice Channels", value=VoiceChannelNumber)
        embed.add_field(name="Total Members", value=f"{allMembers}")
        embed.add_field(name="Humans", value=f"{netUsers}")
        embed.add_field(name="Bots", value=f"{botUsers}")
        embed.add_field(name="Emojis", value=emojis)
        embed.add_field(name="Verification Level", value=verification)
        embed.add_field(name=f'Roles', value=guildroles, inline=False)
        embed.set_footer(text=f"ID: {ctx.guild.id} | {server_created_at}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    # Prune
    @commands.command()
    @commands.guild_only()
    async def prune(self,ctx, limit):
        try:
            await ctx.channel.purge(limit=int(limit)+1)
        except ValueError:
            if str(limit.lower())=="all":    
                await ctx.channel.clone()
                await ctx.channel.delete()
            else:
                await ctx.send("Wrong argument given")    
        else:        
            await ctx.send(f'Cleared by {ctx.author.name}',delete_after = 2)

    # Ban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True) 
    async def ban(self, ctx, user: discord.Member, *, reason:str = "No reason specified"):
        embed = discord.Embed(title="Member Banned", color = 0xD82626)
        embed.add_field(name="Member:", value=f"{user.name}#{user.discriminator} ", inline=True)
        embed.add_field(name="Banned by:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await user.send(f"You are banned from the server. \nReason: {reason}")   
        await user.ban()

    # Unban
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True) 
    async def unban(self,ctx,user:str):
        entries = await ctx.guild.bans()
        l = []
        for entry in entries:
            member = f"{entry.user.name}#{entry.user.discriminator}"
            l.append(member)
        if user in l:
            for e in entries:
                t = f"{e.user.name}#{e.user.discriminator}"
                if  t == user:
                    
                    await ctx.guild.unban(e.user)  
                    await ctx.send("Member unbanned")   
        else:
            await ctx.send("Cannot find user in list of banned members. \nEnter the username in this format: name#discriminator(eg:rob#1212)")   

    # Kick
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        embed = discord.Embed(title="Member Kicked", color = 0x3C80E2)
        embed.add_field(name="Member:", value=f"{user.name}#{user.discriminator} ", inline=True)
        embed.add_field(name="Kicked by:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await user.send(f"You have been kicked from the server. \nReason: {reason}")   
        await user.kick()  

    # Throw error
    @ban.error
    async def ban_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Looks like you forgot to mention the member to be banned. Try again")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Senpai! Senpai doesn't have the permission to use this command") 
        else:
            raise error
    @unban.error
    async def unban_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Looks like you forgot to enter the name of the user to be unbanned. Try again")    

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Senpai! Senpai doesn't have the permission to use this command") 
        else:
            raise error    
    @kick.error
    async def kick_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Looks like you forgot to enter the name of the user to be kicked. Try again")    

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Senpai! Senpai doesn't have the permission to use this command") 
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Sorry, I couldn't find this user")
            
        else:
            raise error 

    # Check bot latency
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong: {round(self.bot.latency*1000)}ms')

    # Get bot invite link
    @commands.command()
    async def invite(self,ctx):
        await ctx.send("Here is my invite link uwu: https://discord.com/api/oauth2/authorize?client_id=641780922445856768&permissions=8&scope=bot")

    # Get Support server invite link
    @commands.command(name = "support",aliases = ['discord'])
    async def support_discord(self,ctx):
        await ctx.send("You are welcome to join our support server: https://discord.gg/CVhk828 \nAnd here is my Sportsbook FULL GUIDE if you are looking for it: https://gist.github.com/Aki176/d1709558004f3c779af4f5f93b7eaf58")

def setup(bot):
    bot.add_cog(Moderation(bot))        
        
