import discord as dis
from discord.ext import commands
import asyncio
import json
import psycopg2
config = json.load(open("testBot.json", "r"))
baseCogs = ["roses"]
con = psycopg2.connect("host='"+config["SQL-host"]+"' port='"+config["SQL-port"]+"' user='"+config["SQL-user"]+"' password='"+config["SQL-pass"]+"'")
cur = con.cursor()
bot = commands.Bot(command_prefix='.')
bot.remove_command("help")
botID = config["id"]
adminID = config["admin"]
discription = config["discription"]
bot.conn = psycopg2.connect("host='"+config["SQL-host"]+"' port='"+config["SQL-port"]+"' user='"+config["SQL-user"]+"' password='"+config["SQL-pass"]+"'")
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

@bot.command(pass_context = True)
async def load(ctx, message):
	try:
		bot.load_extension(message)
	except(AttributeError, ImportError) as e:
		await bot.say("Failed to load: {}, {}".format(type(e), str(e)))
		return
	await bot.say("Loaded {}".format(message))

@bot.command(pass_context = True)
async def unload(ctx, message):
	bot.unload_extension(message)
	await bot.say("Unloaded {}".format(message))

@bot.command(pass_context = True)
async def reload(ctx, message):
	bot.unload_extension(message)
	bot.load_extension(message)
	await bot.say("Reloaded {}".format(message))
	print("\n"*20)

for i in baseCogs:
	try:
		bot.load_extension(i)
		print("{} loaded".format(i))
	except(AttributeError, ImportError) as e:
		print("Failed to load: {}, {}".format(type(e), str(e)))

bot.run(botID)