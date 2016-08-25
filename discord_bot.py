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
    steam = CharField(null=True)
    origin = CharField(null=True)
    battlenet = CharField(null=True)
    uplay = CharField(null=True)

    class Meta:
        database = db

    def create_table_discordname():
        db.connect()
        db.create_tables([DiscordName])
        db.close()


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

        if gp == "steam":
            result = DiscordName.create(discord_name=dn, steam=gt)
        elif gp == "origin":
            result = DiscordName.create(discord_name=dn, origin=gt)
        elif gp == "battlenet":
            result = DiscordName.create(discord_name=dn, battlenet=gt)
        elif gp == "uplay":
            result = DiscordName.create(discord_name=dn, uplay=gt)

        db.close()


    def list_gamertag(self):

        dn = str(input("Type Discord Name: "))

        db.connect()

        try:
            result = DiscordName.get(DiscordName.discord_name == dn)
            return result
        except result.DoesNotExist:
            print (dn + " does not exist")

        db.close()


gt = GamerTag()
# gt.add_gamertag()
gt.list_gamertag()
