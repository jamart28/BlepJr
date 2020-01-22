import discord
from BlepJr import tools, commands

# TODO: Build server structure with sql database; Add message editing and new commands

# NEW COMMANDS: role manager; delete tracker

# Constuction and assignment of the client
BlepJrBot = discord.Client()
# aliasing event wrapper to event
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
    guild.owner.send(f"I'm all alone\n\n{guild.name}")

# Called when messages are sent
@event
async def on_message(msg):
    global reactions
    # server = sql.getServer()
    if msg.author == BlepJrBot.user:
        for reaction in reactions:
            await msg.add_reaction(reaction)
    else:
        if msg.content.startswith(commands.cmd_prefix):
            command, args = tools.parse_message(msg.content[len(commands.cmd_prefix):])
            if command in commands.commands:
                dest, content, embed, reactions = commands.commands[command].run(msg, args)
                await dest.send(content, embed=discord.Embed(description=embed, color=BlepJrBot.color) if embed else embed)

# new on_message after server structure is added (need to finish after deciding how to handle admin commands)
"""
@event
async def on_message(msg):
    global reactions
    guild = server.Server.getServer(msg.guild.id)
    if msg.author == BlepJr.user:
        for reaction in reactions:
            await msg.add_reaction(reaction)
    else:
        if msg.content.startswith(guild.cmd_prefix):
            command, args = tools.parse_message(msg.content[len(guild.cmd_prefix):])
            if command in command.commands:
                if !command.needsAdmin or
                    (command.needsAdmin and msg.user in server.admins):
                    dest, content, embed, reactions = commands.commands[commands].run(msg, args)
"""


BlepJrBot.run(tools.read_file('BOT_TOKEN.txt'))
