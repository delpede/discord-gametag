#!/usr/local/bin/python3

'''
A gamertag Discord Bot
'''

import sqlite3
from peewee import *

db = SqliteDatabase('discord_bot.db')


class DiscordName(Model):
    id = IntegerField(primary_key=True)
    discord_name = CharField(unique=True)
    steam = CharField
    origin = CharField
    battlenet = CharField
    uplay = CharField

    class Meta:
        database = db


class GamerTag():
    '''
    This class handles everything related to gamertags.
    '''

    def add_gamertag(self):
        try:
            dn = str(input("Discord name: "))
            gp = input("Game Platform: ")
            gt = input("Gamer Tag: ")
        except Exception as e:
            print (e)
            # return add_gamertag(self)

        db.connect()
        db.create_tables([DiscordName])

        result = DiscordName.create(discord_name=dn, steam=gt)
        db.close()


gt = GamerTag()
gt.add_gamertag()
