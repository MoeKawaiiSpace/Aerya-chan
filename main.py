import discord
import datetime
import asyncpg
from discord.ext import commands


bot = commands.Bot(command_prefix='a!')
bot.remove_command("help")
bot.start_time = datetime.datetime.utcnow()
init_extensions = ['cogs.moderation','cogs.fun']

async def create_db_pool():
    url = 'postgres://fjxgshqttypeqy:6dd48327fcd4c0f72ef84f3128faa2cbbefbe4e50051b8ede1f2bb4dc2077302@ec2-34-200-15-192.compute-1.amazonaws.com:5432/deblq12pln1fou'
    bot.pg_con = await asyncpg.create_pool(host = '167.71.99.250',user = 'postgres', password = 'postgres',database = 'aerya')

if __name__ == '__main__':
    for extension in init_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print("Ready")        
@bot.event
async def on_guild_join(guild):
    check = await bot.pg_con.fetch("SELECT toggle from matchbet WHERE guild_id = $1",guild.id)
    if check == None:
        await bot.pg_con.execute("INSERT INTO matchbet(guild_id,toggle,channel_id) VALUES($1,'off',None)",guild.id)

@bot.event
async def on_message(message):
    if message.guild is not None:
        ctx = await bot.get_context(message)
        if ctx.valid:
            check1 = await bot.pg_con.fetch("SELECT * FROM profile_ext WHERE user_id = $1",ctx.author.id)
            check2 = await bot.pg_con.fetch("SELECT * FROM profiles WHERE user_id = $1 AND guild_id = $2",ctx.author.id,ctx.guild.id)
            if not check2: 
                await bot.pg_con.execute("INSERT INTO profiles(user_id,guild_id,xp) VALUES($1,$2,0)",ctx.author.id,ctx.guild.id)

            if not check1:
                await bot.pg_con.execute("INSERT INTO profile_ext(user_id, description, waifus, birthday,reputation,badges,bal)  VALUES($1, 'No description given','No waifus/husbandos','Birthday not set',0,$2::TEXT[],10000)",ctx.author.id,[])    
    
       
    await bot.process_commands(message)    
    
bot.loop.run_until_complete(create_db_pool())          
bot.run("NjQxNzgwOTIyNDQ1ODU2NzY4.XxhT3Q.wwsjSvNzBrcjKuRrm1OnZSNZqg4")    