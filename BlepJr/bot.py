import discord


class bot:
    def __init__(self, color, invite):
        """Constructs bot object
        param=color: Color representing bot; prefix: string representing expected prefix for commands, invite: invite link for bot represented as a string
        """
        self.client = discord.Client()
        self.color = color
        self.invite_link = invite

    def run(self, token):
        """Starts the client up
        param=token: token to connect to bot as a string
        """
        self.client.run(token)
