import sqlite3
from discord import Color, Guild
from dataclasses import dataclass


@dataclass
class Server:
    guild: Guild
    cmd_prefix: str
    color: Color
    admins: list
    mods: list

    _db = 'blepjr.db'

    def add(self):
        """Adds this server to the bot's database
        """
        conn = sqlite3.connect(self._db)
        crsr = conn.cursor()

        r, g, b = self.color.to_rgb()
        crsr.execute(
            'INSERT INTO servers\n'
            f'VALUES ({self.guild.id}, "{self.cmd_prefix}", {r}, {g}, {b});'
        )

        for mod in self.mods:
            crsr.execute(
                'INSERT INTO mods\n'
                f'VALUES ({mod.id}, 0, {self.guild.id});'
            )

        for admin in self.admins:
            crsr.execute(
                'UPDATE mods\n'
                'SET admin=1\n'
                f'WHERE user_id={admin.id} AND server_id={self.guild.id};'
            )

        conn.commit()
        conn.close()

        print(f'Server {self.guild.id} added to database {self._db}')

    def delete(self):
        """Deletes this server from the bot's database
        """
        conn = sqlite3.connect(self._db)
        crsr = conn.cursor()

        crsr.execute(f'DELETE FROM servers WHERE id={self.id};')

        conn.commit()
        conn.close()

        print(f'Server {self.guild.id} deleted from {self._db}')

    @classmethod
    def getServer(cls, guild):
        """Retrieves a server with the given id from the bot's database and constructs server object

        Args:
            id: int representing the servers unique id
        """
        conn = sqlite3.connect(cls._db)
        crsr = conn.cursor()

        crsr.execute(
            'SELECT *\n'
            'FROM servers\n'
            f'WHERE id={guild.id};'
        )

        results = crsr.fetchone()
        cmd_prefix = results[1]
        color = Color.from_rgb(results[2], results[3], results[4])

        crsr.execute(
            'SELECT *\n'
            'FROM mods\n'
            f'WHERE server_id={guild.id};'
        )

        results = crsr.fetchall()
        admins = [guild.get_member(result[0]) for result in results if result[1]]
        mods = [guild.get_member(result[0]) for result in results]

        return cls(guild, cmd_prefix, color, admins, mods)

    def welcome(self):
        """Returns welcome message as a string
        """
        return (
            'Hi! Thank you for inviting me to your server. I can be used for general moderation '
            'and some other neat tricks. A full list of my functionality is below and can be '
            'accessed again by typing `!help`. If you have any questions, you can join my support '
            'server to contact my developer and get updates on outages and new features or changes '
            'as they are added: https://discord.gg/BDKn2Q5. Enjoy discording!'
        )

    def bye(self):
        """Returns bye message as a string
        """
        return (
            "Thank you for your use of me. If there was anyting I could've done better or "
            'any specifc reason I was left behind, please be sure to let my developer know at '
            'the support server for this bot: https://discord.gg/BDKn2Q5.'
        )
