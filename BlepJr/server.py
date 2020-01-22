import discord
import sqlite3

def addServer(guild):
    # sql magic probably
    pass

@dataclass
class Server:
    guild_id: int
    cmd_prefix: str
    color: discord.Color
    admins: list
    mods: list

    def add(self):
        # magically convert the thing to sql
        pass

    def update(self):
        # magically update the sql
        pass

    def delete(self):
        # magically delete the server from sql
        pass

    @classmethod
    def getServer(cls):
        # magically get the server from sql
        return cls()
