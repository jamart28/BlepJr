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
        return (
            f'{self.usage}\n'
            f'{self.description}\n'
            f'{self.parameters}\n\n'
        )

    @abstractmethod
    async def send(self, msg, args):
        pass


class Help(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}help (here)`'
        self.description = 'Sends this message to you'
        self.subcommands = None
        self.parameters = '• `here`: Sends message to channel instead'
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
            'Key:\n• `[]`: Required parameter\n• `{}`: Optional parameter\n• `()`: Flag; these are '
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


class Poll(command):
    def __init__(self, server):
        self.usage = (
            f'`{server.cmd_prefix}poll [Title] "{{Emote}} [Option]" "{{Emote}} [Option]"...`'
        )
        self.description = 'Sends a poll'
        self.subcommands = None
        self.parameters = (
            '• `Title`: Poll being posed\n• `Emote`: Emote representing the option\n• `Option`: '
            'Poll option'
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


class Invite(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}invite (here)`'
        self.description = "Sends this bot's invite link to you"
        self.subcommands = None
        self.parameters = '• `here`: Sends message to channel instead'
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


class Mod(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}mod [subcommand] [user]...`'
        self.description = 'Configures what users are able to use my admin commands'
        self.subcommands = {
            'add': self.add,
            'delete': self.delete,
            'show': self.show,
        }
        subcommands = ', '.join(f'`{subcommand}`' for subcommand in self.subcommands)
        self.parameters = (
            '• `subcommand`: Subcommand to run for configuring admins; valid subcommands: '
            f"{subcommands}\n• `user`: Mentioned (@'ed) user **or** role to be configured\nNote: "
            'All commands below this one, as well as this command, can only be done by bot mods'
        )
        self.server = server

    def add(self, mods):
        pass

    def delete(self, mods):
        pass

    def show(self, mods):
        pass

    async def send(self, msg, args):
        if args[0]:
            subcommand = args.pop(0).lower()
            if subcommand in self.subcommands:
                self.subcommands[subcommand](args)
            else:
                await msg.channel.send(
                    f"`{subcommand}` isn't a valid subcommand. Valid subcommands are:\n• `add`: "
                    'add a new user or role to the list of mods\n• `delete`: Delete a user or '
                    'role from the list of mods\n• `show`: Show the list of mod users and roles'
                )
        else:
            await msg.channel.send(
                'No subcommand was given. Valid subcommands are:\n• `add`: add a new user or role'
                'to the list of mods\n• `delete`: Delete a user or role from the list of mods\n'
                '• `show`: Show the list of mod users and roles'
            )


class Admin(command):
    def __init__(self, server):
        self.usage = f'`{server.cmd_prefix}admin [subcommand] [user]...`'
        self.description = 'Configures what users are able to use my admin commands'
        self.subcommands = {
            'add': self.add,
            'delete': self.delete,
            'show': self.show,
        }
        subcommands = ', '.join(f'`{subcommand}`' for subcommand in self.subcommands)
        self.parameters = (
            '• `subcommand`: Subcommand to run for configuring admins; valid subcommands: '
            f"{subcommands}\n• `user`: Mentioned (@'ed) user **or** role to be configured\nNote: "
            'All commands below this one, as well as this command, can only be done by bot admins '
            'or users with the `Administrator` permission'
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
                    'role from the list of admins\n• `show`: Show the list of admin users and roles'
                )
        else:
            await msg.channel.send(
                'No subcommand was given. Valid subcommands are:\n• `add`: add a new user or role'
                'to the list of admins\n• `delete`: Delete a user or role from the list of admins\n'
                '• `show`: Show the list of admin users and roles'
            )



def getCommands(server):
    return {
        'help': Help(server),
        'poll': Poll(server),
        'invite': Invite(server),
        'admin': Admin(server),
    }
