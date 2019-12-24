import emojis

def read_file(file):
    """Reads file and returns content
    param=file: file name as a string
    returns=string representing file content
    """
    with open(file) as read_file:
        return read_file.read().rstrip()

def parse_message(msg, prefix):
    """Parses message into command and args
    param=msg: message sent by user; prefix: command prefix as a string
    returns=tuple containing the command as a string and the arguments as a list
    """
    # gets rid of the prefix
    msg = msg[len(prefix):]
    # splits arguments and command
    msg = [mstrip for m in msg.split('"') if (mstrip := m.strip())]
    return msg[0].lower(), msg[1:]

def parse_emotes(args):
    """Parses emotes from arguments
    param=args: string array representing arguments, generally from parse_args()
    returns=string list with the new arguments, emotes list, and default emotes
    """
    # default emotes if one isn't given
    default = iter('🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿')
    # list to hold the new arguments in tuple form (emote, arg)
    new_args = []
    # cosntructing new arguments and emote list
    for arg in args:
        # argument uses a guild emote
        if '>' in arg:
            arg = arg.split('>')
            new_args.append((f'{arg[0].strip()}>', arg[1].strip()))
        # argument uses a general emote
        elif emojis.get(arg.split()[0]):
            arg = arg.split(maxsplit=1)
            new_args.append((arg[0].strip(), arg[1].strip()))
        # argument does not specify an emote
        else:
            new_args.append((next(default), arg.strip()))
    return new_args
