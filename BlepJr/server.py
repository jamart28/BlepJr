import discord
import sqlite3
from dataclasses import dataclass

@dataclass
class Server:
    id: int
    cmd_prefix: str
    color: discord.Color
    admins: list
    mods: list

    _db = 'blepjr.db'

    def add(self):
        """Adds this server to the bot's database
        """
        conn = sqlite3.connect(self._db)
        crsr = conn.cursor()

        crsr.execute('INSERT INTO servers\n'
                     f'VALUES ({self.id}, "{self.cmd_prefix}", "{self.color.to_rgb()}");'
        )

        for mod in self.mods:
            crsr.execute('INSERT INTO mods\n'
                         f'VALUES ({admin.id}, 0, {self.id});'
            )

        for admin in self.admins:
            crsr.execute('UPDATE mods\n'
                          'SET admin=1\n'
                         f'WHERE user_id={admin.id} AND server_id={self.id};'
            )

        conn.commit()
        conn.close()

        print(f'Server {self.id} added to database {self._db}')

    def delete(self):
        """Deletes this server from the bot's database
        """
        conn = sqlite3.connect(self._db)
        crsr = conn.cursor()

        crsr.execute(f'DELETE FROM servers WHERE id={self.id};')
        crsr.execute(f'DELETE FROM mods WHERE id={self.id};')

        conn.commit()
        conn.close()

        print(f'Server {self.id} deleted from {self._db}')

    @classmethod
    def getServer(cls, id):
        """Retrieves a server with the given id from the bot's database and constructs server object

        Args:
            id: int representing the servers unique id
        """
        conn = sqlite3.connect(cls._db)
        crsr = conn.cursor()

        crsr.execute('SELECT *\n'
                      'FROM servers\n'
                     f'WHERE id={id};'
        )

        results = crsr.fetchone()

        # Assign things here
        # printing results temporarily to see structure

        crsr.execute('SELECT *\n'
                      'FROM mods\n'
                     f'WHERE id={id};'
        )

        results = crsr.fetchall()

        # Assign things here
        # printing results temporarily to see structure

        return cls(id, cmd_prefix, color, admins, mods)
