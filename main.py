import discord
from BlepJr.server import Server
from BlepJr.tools import read_file, parse_message
from BlepJr.commands import getCommands

BlepJrBot = discord.Client()
event = BlepJrBot.event


# Called when bot is ready
@event
async def on_ready():
    print("I'm ready")
    print(BlepJrBot.user)
    print(discord.version_info)
    print(discord.__version__)


# Called when bot joins a cuild
@event
async def on_guild_join(guild):
    server = Server(guild.id, "!", discord.Color.blurple(), [guild.owner], [guild.owner])
    server.add()
    await guild.owner.send(f"I'm all alone\n\n{guild.name}")


@event
async def on_message(msg):
    server = Server.getServer(msg.guild.id)
    if msg.author != BlepJrBot.user:
        if msg.content.startswith(server.cmd_prefix):
            command, args = parse_message(msg.content[len(server.cmd_prefix):])
            commands = getCommands(server)
            if command in commands:
                await commands[command].send(msg, args)


BlepJrBot.run(read_file('BOT_TOKEN.txt'))
