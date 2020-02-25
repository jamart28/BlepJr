import emojis


def read_file(file):
    """Reads file and returns contents within

    Args:
        file: String representing file to be read

    Returns:
        String representing content within the file
    """
    with open(file) as read_file:
        return read_file.read().rstrip()


def parse_message(msg):
    """Parses message into command and args

    Args:
        msg: String representing message sent by the user

    Returns:
        Tuple containing the command as a string and the arguments as a list
    """
    # splits arguments and command
    msg = [mstrip for m in msg.split() if (mstrip:= m.strip())]
    i = 1

    while i < len(msg):
        if msg[i].startswith('"'):
            j = i
            while not msg[j].endswith('"') and j < len(msg):
                j += 1
            msg[i] = " ".join(msg[i:(j+1)]).strip('"')
            del msg[(i+1):(j+1)]
        elif msg[i].startswith("'"):
            j = i
            while not msg[j].endswith("'") and j < len(msg):
                j += 1
            msg[i] = " ".join(msg[i:(j+1)]).strip("'")
            del msg[(i+1):(j+1)]

        i += 1

    return msg[0].lower(), msg[1:]


def parse_emotes(args):
    """Parses emotes from arguments

    Args:
        args: List of strings representing arguments from parse_message()

    Returns:
        List of tuples where each tuple pair representing ({emote}, {argument})
    """
    # default emotes if one isn't given
    default = iter('🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿')

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
    return new_args
