from BlepJr import bot, tools, commands

# TODO: Add message editing and new commands

# NEW COMMANDS: role manager; delete tracker

# Constuction and assignment of the bot
BlepJrBot = bot.bot(bot.discord.Color.blurple(), 'https://discordapp.com/api/oauth2/authorize?client_id=646783589710692399&permissions=1476914391&scope=bot')
# aliasing event wrapper to event
event = BlepJrBot.client.event

# Called when bot is ready
@event
async def on_ready():
    print("I'm ready")
    print(BlepJrBot.client.user)
    print(bot.discord.version_info)
    print(bot.discord.__version__)

# Called when bot joins a cuild
@event
async def on_guild_join(guild):
    guild.owner.send(f"I'm all alone\n\n{guild.name}")

# Called when messages are sent
@event
async def on_message(msg):
    global out
    if msg.author == BlepJrBot.client.user:
        for reaction in out[3]:
            await msg.add_reaction(reaction)
    else:
        if msg.content.startswith(commands.cmd_prefix):
            command, args = tools.parse_message(msg.content, commands.cmd_prefix)
            if command in commands.commands:
                out = commands.commands[command].run(msg, args)
                await out[0].send(out[1], embed=bot.discord.Embed(description=out[2], color=BlepJrBot.color))

BlepJrBot.run(tools.read_file('BOT_TOKEN.txt'))
