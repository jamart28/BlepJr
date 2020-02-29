from discord import Embed
from abc import ABC, abstractmethod
from BlepJr.tools import parse_emotes


# Unsure if needed
def needsAdmin(method):
    async def admin_method(self, msg, args):
        if msg.author in self.server.admins or msg.author.permissions_in(msg.channel).administrator:
            self.method(msg, args)

    return admin_method


def needsMod(method):
    async def mod_method(self, msg, args):
        if msg.author in self.server.mods:
            self.method(msg, args)

    return mod_method


class command(ABC):
    def help(self):
        """Returns string representing help information for this command
        """
        if self.subcommands:
            subcommands = ''
            for subcommand in self.subcommands:
                subcommands += f'`{subcommand}`, '
            subcommands.rstrip(', ')
            return (
                f'{self.usage}\n'
                f'{self.description}\n'
                f'Subcommands: {subcommands}\n'
                f'Parameters: {self.parameters}\n\n'
            )
        else:
            return (
                f'{self.usage}\n'
                f'{self.description}\n'
                f'Parameters: {self.parameters}\n\n'
            )

    @abstractmethod
    async def send(self, msg, args):
        pass


class help(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}help (here)`'
        self.description = 'Sends this message to you'
        self.subcommands = None
        self.parameters = '`here`: Sends message to channel instead'
        self.server = server

    def help(self):
        return super().help()

    def build_help_msg(self):
        """Uses command classes to build a help message for the commands implemented by this bot
        """
        self.help_msg = 'The following are the commands implemented by this bot.\n\n'
        for command in getCommands(self.server).values():
            self.help_msg += command.help()
        self.help_msg += (
            'Key:\n`[]`: Required parameter\n`{}`: Optional parameter\n`()`: Flag; these are '
            'optional in nature and triggered by typing the weird exact\nNote: All multi-word '
            'arguments must be enclosed by either double-quotes or single-quotes.'
        )

    async def send(self, msg, args):
        """Sends help message to the specified location

        Args:
            msg: `discord.Message` object representing message sent by the user
            args: List of strings representing the arguments parsed from the above message
        """
        self.build_help_msg()
        if args and args[0].lower() == 'here':
            await msg.channel.send(embed=Embed(description=self.help_msg, color=self.server.color))
        else:
            await msg.author.send(embed=Embed(description=self.help_msg, color=self.server.color))


class poll(command):
    def __init__(self, server):
        self.usage = (
            f'`{server.cmd_prefix}poll [Title] "{{Emote}} [Option]" "{{Emote}} [Option]"...`'
        )
        self.description = 'Sends a poll'
        self.subcommands = None
        self.parameters = (
            "\n• `Title`: Poll being posed\n• `Emote`: Emote representing the option\n• `Option`: Poll "
            "option"
        )
        self.server = server

    def help(self):
        return super().help()

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

        bot_msg = await msg.channel.send(
            title, embed=Embed(description=poll, color=self.server.color)
        )
        for reaction in reactions:
            await bot_msg.add_reaction(reaction)


class invite(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}invite (here)`'
        self.description = "Sends this bot's invite link to you"
        self.subcommands = None
        self.parameters = '`here`: Sends message to channel instead'
        self.server = server
        self.link = 'https://discordapp.com/api/oauth2/authorize?client_id=658913240952340481&permissions=268766294&scope=bot'

    def help(self):
        return super().help()

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


class admin(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}admin [subcommand] [user]...`'
        self.description = 'Configures what users are able to use my admin commands'
        self.subcommands = {
            'add': self.add,
            'delete': self.delete,
            'show': self.show,
        }
        self.parameters = (
            "`user`: User **or** role to be configured, must be mentioned (@'ed)\nNote: admins are "
            'considered to be mods as well and thus able to run all mod commands in addition to '
            'admin commands.'
        )
        self.server = server

    def add(self, admins):
        for admin in admins:
            pass

    def delete(self, admins):
        pass

    def show(self, admins):
        pass

    async def send(self, msg, args):
        if args[0]:
            subcommand = args.pop(0).lower()
            if subcommand in self.subcommands:
                self.subcommands[subcommand](args)
            else:
                await msg.channel.send(
                    f"`{subcommand}` isn't a valid subcommand. Valid subcommands are:\n• `add`: "
                    'add a new user or role to the list of admins\n• `delete`: Delete a user or '
                    'role from the list of admins\n• `show`: Show the full list of admin users and '
                    'roles or show the status of a user or role (whether they are on the list)'
                )
        else:
            await msg.channel.send(
                'No subcommand was given. Valid subcommands are:\n• `add`: add a new user or role'
                'to the list of admins\n• `delete`: Delete a user or role from the list of admins\n'
                '• `show`: Show the full list of admin users and roles or show the status of a '
                'user or role (whether they are on the list)'
            )



def getCommands(server):
    return {
        'help': help(server),
        'poll': poll(server),
        'invite': invite(server),
        'admin': admin(server),
    }
