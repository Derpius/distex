from sympy import preview
import discord
from io import BytesIO
import re
import os
import signal
import sys
from dotenv import load_dotenv

def onExit(_signo, _stack_frame):
	print("Performing safe shutdown")
	sys.exit(0)

signal.signal(signal.SIGINT, onExit)
signal.signal(signal.SIGTERM, onExit)

load_dotenv()

latexPattern = re.compile(r"```latex\n.*?```", re.S)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(msg: discord.Message):
	'''Convert LaTeX input to an image and reply with it'''
	if msg.author.id == client.user.id: return

	files = []
	for match in latexPattern.finditer(msg.content):
		buf = BytesIO()

		try:
			preview(
				f"$${match.group(0)[9:-3]}$$",
				output="png", viewer="BytesIO", outputbuffer=buf,
				euler=False,
				dvioptions=["-D", "160", "-bg", "Transparent", "-fg", "rgb 0.8666666666666667 0.8705882352941177 0.8745098039215686"]
			)
		except RuntimeError as err:
			await msg.reply("Invalid syntax")
			print(err)
			return

		buf.seek(0)
		files.append(discord.File(fp=buf, filename="latex.png"))

	if files: await msg.reply(files=files)

token = os.getenv("DISTEX_TOKEN")
if token is None:
	print("DISTEX_TOKEN is not set")
	sys.exit(1)

client.run(token)
