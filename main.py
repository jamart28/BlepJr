import discord
from BlepJr.server import Server
from BlepJr.tools import read_file, parse_message
from BlepJr.commands import getCommands


BlepJrBot = discord.Client()
event = BlepJrBot.event


@event
async def on_ready():
    print("I'm ready")
    print(BlepJrBot.user)
    print(discord.version_info)
    print(discord.__version__)


@event
async def on_guild_join(guild):
    server = Server(guild, "!", discord.Color.blurple(), [], [])
    server.add()
    await guild.owner.send(server.welcome())
    await guild.owner.send(
        embed=Embed(description=getCommands(server)['help'].build_help_msg(), color=server.color)
    )


@event
async def on_guild_remove(guild):
    Server.getServer(guild.id).delete()


@event
async def on_message(msg):
    server = Server.getServer(msg.guild)
    if msg.author != BlepJrBot.user:
        if msg.content.startswith(server.cmd_prefix):
            commands = getCommands(server)
            command, args = parse_message(msg.content[len(server.cmd_prefix):])
            if command in commands:
                await commands[command].send(msg, args)


BlepJrBot.run(read_file('BOT_TOKEN.txt'))
