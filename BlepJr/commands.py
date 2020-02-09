from discord import Embed
from abc import ABC, abstractmethod
from BlepJr.tools import parse_emotes

# Unsure if needed
"""def adminCommand(cls):
    cls.needsAdmin = True
    return cls

def userCommand(cls):
    cls.needsAdmin = False
    return cls"""

class command(ABC):
    def help(self):
        """Returns string representing help information for this command
        """
        return(f'Name: {self.name}\n'
               f'Description: {self.description}\n'
               f'Parameters: {self.parameters}\n'
               f'Usage: {self.usage}\n\n')

    @abstractmethod
    async def send(self, msg, args):
        pass


class help(command):
    def __init__(self, server):
        self.name = 'Help'
        self.description = 'Sends information on commands (sends directly to user by default)'
        self.parameters = 'us": (optional) sends message to channel'
        self.usage = f'`{server.cmd_prefix}help`, `{server.cmd_prefix}help "us"`'
        self.server = server

    def build_help_msg(self):
        """Uses command classes to build a help message for the commands implemented by this bot
        """
        self.help_msg = 'The following are the commands implemented by this bot.\n\n'
        for command in getCommands(self.server).values():
            self.help_msg += command.help()

    async def send(self, msg, args):
        """Sends help message to the specified location

        Args:
            msg: `discord.Message` object representing message sent by the user
            args: List of strings representing the arguments parsed from the above message
        """
        self.build_help_msg()
        if args and args[0].lower() == 'us':
            await msg.channel.send(embed=Embed(description=self.help_msg, color=self.server.color))
        else:
            await msg.author.send(embed=Embed(description=self.help_msg, color=self.server.color))


class poll(command):
    def __init__(self, server):
        self.name = 'Poll'
        self.description = 'Sends a poll as a reactable message'
        self.parameters = ("Title: What's being polled; Emote: (optional for each option) Emote "
                           "representing the option; Option: option being voted on")
        self.usage = (f'Usage: `{server.cmd_prefix}poll "Is this a title" ":thumbsup:: Ye" '
                      f'":thumbsdown:: Nah"`, `{server.cmd_prefix}poll "This is a title" "Ye" "Nah"`')
        self.server = server

    async def send(self, msg, args):
        """Sends poll message to the channel of `msg` and reacts with approriate emotes for options

        Args:
            msg: `discord.Message` object representing message sent by the user
            args: List of strings representing the arguments parsed from the above message
        """
        title = f'**:bar_chart:{args[0]}**'
        args = parse_emotes(args[1:])

        reactions = [emote for emote, not_used in args]
        poll = '\n'.join([f'{emote} {option}' for emote, option in args])

        bot_msg = await msg.channel.send(title, embed=Embed(description=poll, color=self.server.color))
        for reaction in reactions:
            await bot_msg.add_reaction(reaction)


class invite(command):
    def __init__(self, server):
        self.name = 'Invite'
        self.description = 'Sends the invite link for the bot'
        self.parameters = '"us": (optional) sends message to channel'
        self.usage = f'Usage: `{server.cmd_prefix}invite`, `{server.cmd_prefix}invite "us"`'
        self.server = server
        self.link = 'https://discordapp.com/api/oauth2/authorize?client_id=658913240952340481&permissions=268766294&scope=bot'

    async def send(self, msg, args):
        """Sends invite link for this bot to the specified designation

        Args:
            msg: `discord.Message` object representing message sent by the user
            args: List of strings representing the arguments parsed from the above message
        """
        if args and args[0].lower() == 'us':
            await msg.channel.send(self.link)
        else:
            await msg.author.send(self.link)

def getCommands(server):
    return {
        'help': help(server),
        'poll': poll(server),
        'invite': invite(server),
    }
