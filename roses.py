import discord as dis
from discord.ext import commands
import json
import psycopg2
from random import randrange
import time

class Roses():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True)
	async def rosesarered(self, ctx, message):
		cur = self.bot.conn.cursor()
		self.bot.conn.commit()
		cur.execute("CREATE TABLE IF NOT EXISTS roses(id INT, line2 VARCHAR, line3 VARCHAR, line4 VARCHAR)")
		y = ctx.message.content[13:]
		x = y.split(",")

		if len(x) == 3 or len(x) == 2:
			x[1] = x[1][1:]
			self.bot.conn.commit()
			cur.execute("SELECT id FROM roses")
			num = len(cur.fetchall()) + 1
			self.bot.conn.commit()
			if len(x) == 3:
				cur.execute("SELECT id FROM roses WHERE line2=('{}') AND line3=('{}') AND line4=('{}')".format(x[0], x[1], x[2]))
			else:
				cur.execute("SELECT id FROM roses WHERE line2=('{}') AND line3=('{}')".format(x[0], x[1]))
			check = len(cur.fetchall())
			if check > 0:
				await self.bot.say("poem already exists")
			else:
				self.bot.conn.commit()
				if len(x) == 3:
					x[2] = x[2][1:]
					cur.execute("INSERT INTO roses(id, line2, line3, line4) VALUES ('{}', '{}', '{}', '{}')".format(num, x[0], x[1], x[2]))
				else:
					cur.execute("INSERT INTO roses(id, line2, line3) VALUES ('{}', '{}', '{}')".format(num, x[0], x[1]))
				await self.bot.say("poem added")
		else:
			await self.bot.say("invalid syntax, useage: .rosesarered line#2, line#3, line#4")

	@commands.command(pass_context=True)
	async def roses(self):
		cur = self.bot.conn.cursor()
		self.bot.conn.commit()
		cur.execute("SELECT id FROM roses")
		num = randrange(1, len(cur.fetchall())+1)
		self.bot.conn.commit()
		cur.execute("SELECT line2, line3, line4 FROM roses WHERE id={}".format(num))
		poem = cur.fetchone()
		await self.bot.say("roses are red")
		for i in poem:
			time.sleep(1)
			await self.bot.say(i)

def setup(bot):
	bot.add_cog(Roses(bot))