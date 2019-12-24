from . import tools
# command prefix
cmd_prefix = '!'

"""
Classes representing the commands the bot is able
"""
class help:
    # Command information (Used by the help command)
    name = 'Help'
    description = 'Sends information on commands (sends directly to user by default)'
    arguments = '"us": (optional) sends message to channel'
    usage = f'`{cmd_prefix}help`, `{cmd_prefix}help "us"`'

    # message which contains all the help information; Built by function below
    __help_msg = 'The following are the commands implemented by this bot.\n\n'

    @classmethod
    def build_help_msg(cls):
        """Builds the help message to be sent by run (class method due to changing a class variable)
        """
        if cls.__help_msg == 'The following are the commands implemented by this bot.\n\n':
            for command in commands.values():
                cls.__help_msg += f'name: {command.name}\nDescription: {command.description}\nParameters: {command.arguments}\nUsage: {command.usage}\n\n'

    @classmethod
    def run(cls, msg, args):
        """Sends message to user or channel with informatoin on all commands implemented by the bot (class method due to using a class variable)
        param=msg: message sent; args: arguments parsed from message sent
        returns=tuple representing the output to discord - destination, msg, embed, reactions
        """
        cls.build_help_msg()
        if args and args[0].lower() == 'us':
            return msg.channel, '', cls.__help_msg, []
        else:
            return msg.author, '', cls.__help_msg, []

class poll:
    # Command information (Used by the help command)
    name = 'Poll'
    description = 'Sends a poll as a reactable message'
    arguments = "Title: What's being polled; Emote: (optional for each option) Emote representing the option; Option: option being voted on"
    usage = f'`{cmd_prefix}poll "Is this a title" ":thumbsup:: Ye" ":thumbsdown:: Nah"`, `{cmd_prefix}poll "This is a title" "Ye" "Nah"`'

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


# commands implemented by bot in the form of a dictionary - values are classes
commands = {
    'help': help,
    'poll': poll
}
