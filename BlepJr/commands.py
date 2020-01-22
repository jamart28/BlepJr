import discord
from . import tools

def adminCommand(cls):
    cls.needsAdmin = True
    return cls

def userCommand(cls):
    cls.needsAdmin = False
    return cls

"""WIP"""
class output:
    def __init__(destination, msg, embed, reactions):
        self.destination = destination
        self.message = msg
        self.embed = embed
        self.reactions = reactions


"""
Classes representing the commands the bot is able
"""
class help:
    @staticmethod
    def help(cmd_prefix):
        """Returns string representing help information for this command

        Args:
            cmd_prefix: String representing the prefix before the command
        """
        return ('Name: Help\n'
                'Description: Sends information on commands (sends directly to user by default)\n'
                'Parameters: "us": (optional) sends message to channel\n'
               f'Usage: `{cmd_prefix}help`, `{cmd_prefix}help "us"`\n\n')

    @staticmethod
    def build_help_msg(cmd_prefix):
        """Builds and returns help message

        Uses command classes to build a help message for the commands implemented by this bot.
        Stores message in class to be sent by the run command

        Args:
            cmd_prefix: String representing the prefix before the command
        """
        help_msg = 'The following are the commands implemented by this bot.\n\n'
        for command in commands.values():
            help_msg += command.help(cmd_prefix)
        return help_msg

    @classmethod
    def run(cls, guild, msg, args):
        """Returns tuple representing to a message representing the help message

        Args:
            msg: discord.Message object representing message sent by the user
            args: List of strings representing the arguments parsed from the above message

        Returns:
            destination, message, embed, reactions:
                destination: Discord object representing where to send the message
                message: String representing message content to send
                embed: String representing content to embed in the message sent
                reactions: List representing emotes to react with
        """
        help_msg = cls.build_help_msg(guild.cmd_prefix)
        if args and args[0].lower() == 'us':
            return msg.channel, '', cls.__help_msg, []
        else:
            return msg.author, '', cls.__help_msg, []

class poll:
    @staticmethod
    def help(cmd_prefix):
        """Returns string representing help information for this command

        Args:
            cmd_prefix: String representing the prefix before the command
        """
        return ('Name: Poll\n'
                'Description: Sends a poll as a reactable message\n'
                "Title: What's being polled; Emote: (optional for each option) Emote representing the option; Option: option being voted on\n"
               f'Usage: `{cmd_prefix}poll "Is this a title" ":thumbsup:: Ye" ":thumbsdown:: Nah"`, `{cmd_prefix}poll "This is a title" "Ye" "Nah"`\n\n')

    @staticmethod
    def run(msg, args):
        """Sends message to channel with reactions to act as a poll
        param=msg: message sent; args: arguments parsed from message sent
        returns=tuple representing the output to discord - destination, msg, embed, reactions
        """
        title = f'**:bar_chart:{args[0]}**'
        args = tools.parse_emotes(args[1:])
        # constucting reaction list from arguments
        reactions = [emote for emote, not_used in args]
        # constructing poll string from arguments
        poll = '\n'.join([f'{emote} {option}' for emote, option in args])
        return msg.channel, title, poll, reactions

class invite:
    @staticmethod
    def help(cmd_prefix):
        """Returns string representing help information for this command

        Args:
            cmd_prefix: String representing the prefix before the command
        """
        return ('Name: Invite\n'
                'Description: Sends the invite link for the bot\n'
                '"us": (optional) sends message to channel\n'
               f'Usage: `{cmd_prefix}invite`, `{cmd_prefix}invite "us"`\n\n')

    @staticmethod
    def run(msg, args):
        """Sends message with bot's invite link to user or channel
        param=msg: message sent; args: arguments parsed from message sent

        Returns:
            destination, message, embed, reactions:
                destination: Discord object representing where to send the message
                message: String representing message content to send
                embed: String representing content to embed in the message sent
                reactions: List representing emotes to react with
        """
        invite_link = 'https://discordapp.com/api/oauth2/authorize?client_id=658913240952340481&permissions=268766294&scope=bot'
        if args and args[0].lower() == 'us':
            return msg.channel, invite_link, None, []
        else:
            return msg.author, invite_link, None, []

# commands implemented by bot in the form of a dictionary - values are classes
commands = {
    'help': help,
    'poll': poll,
    'invite': invite,
}
