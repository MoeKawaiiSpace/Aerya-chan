# Project Name: Aerya
# Last Modified: Sep 27, 2020
# Author: Aki 
# ------------------------

# Import necessary library
import discord
import datetime
import asyncpg
from discord.ext import commands

# Prefix 
bot = commands.Bot(command_prefix='a!')

bot.remove_command("help")
bot.start_time = datetime.datetime.utcnow()
init_extensions = ['cogs.moderation','cogs.fun']

# Connect to PostgreSQL
async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(host = '139.59.251.230',user = 'aki', password = 'vuducanh2003',database = 'aerya')

if __name__ == '__main__':
    for extension in init_extensions:
        bot.load_extension(extension)

# Log when bot is starting
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="https://aerya.moe"))
    print("Daisuki Master-sama, watashi wa Aerya-chan desu!")     
    
# Register the user into the DB when they first time use a bot command
@bot.event
async def on_message(message):
    if message.guild is not None:
        ctx = await bot.get_context(message)
        if ctx.valid:
            check1 = await bot.pg_con.fetch("SELECT * FROM profile_ext WHERE user_id = $1",ctx.author.id)
            check2 = await bot.pg_con.fetch("SELECT * FROM profiles WHERE user_id = $1 AND guild_id = $2",ctx.author.id,ctx.guild.id)
            if not check2: 
                await bot.pg_con.execute("INSERT INTO profiles(user_id,guild_id) VALUES($1,$2)",ctx.author.id,ctx.guild.id)

            if not check1:
                await bot.pg_con.execute("INSERT INTO profile_ext(user_id, description, waifus, birthday,gender,reputation,badges,bal)  VALUES($1,'No description given','No waifus/husbandos','Birthday not set','Gender not set',0,$2::TEXT[],50000)",ctx.author.id,[])    
    
       
    await bot.process_commands(message)    
    
bot.loop.run_until_complete(create_db_pool())    

# Bot token
bot.run("NjQxNzgwOTIyNDQ1ODU2NzY4.XxhT3Q.wwsjSvNzBrcjKuRrm1OnZSNZqg4")    
