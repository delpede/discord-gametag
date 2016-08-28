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

    def check_discord_name(self, dn):

        db.connect()
        result = DiscordName.select().where(DiscordName.discord_name == dn)

        try:
            user = result.where(DiscordName.discord_name == dn).get()
            print("Found user " + user.discord_name)
            return 1
        except DiscordName.DoesNotExist:
            print("Did not find " + dn)
            return 0

        db.close()


    def add_gamertag(self):
        try:
            dn = str(input("Discord name: "))
            gp = input("Game Platform: ")
            gt = input("Gamer Tag: ")

            # return add_gamertag(self)

            db.connect()
            result = DiscordName.select().where(DiscordName.discord_name == dn)

            try:
                user = result.where(DiscordName.discord_name == dn).get()
                print("Found user " + user.discord_name)
                print ("updating")

                if gp == "steam":
                    result = user.discord_name.steam(gt)
                elif gp == "origin":
                    result = DiscordName.create(discord_name=dn, origin=gt)
                elif gp == "battlenet":
                    result = DiscordName.create(discord_name=dn, battlenet=gt)
                elif gp == "uplay":
                    result = DiscordName.create(discord_name=dn, uplay=gt)
            except DiscordName.DoesNotExist:
                print ("Creating")
                if gp == "steam":
                    result = DiscordName.create(discord_name=dn, steam=gt)
                elif gp == "origin":
                    result = DiscordName.create(discord_name=dn, origin=gt)
                elif gp == "battlenet":
                    result = DiscordName.create(discord_name=dn, battlenet=gt)
                elif gp == "uplay":
                    result = DiscordName.create(discord_name=dn, uplay=gt)

        except Exception as e:
            print (e)

        db.close()


    def list_gamertag(self):

        dn = str(input("Type Discord Name: "))

        db.connect()

        result = DiscordName.select().where(DiscordName.discord_name == dn)

        try:
            user = result.where(DiscordName.discord_name == dn).get()
            print ("Found user " + user.discord_name)
            gamertag_result = DiscordName.select(DiscordName.steam).where(DiscordName.discord_name == user.discord_name)
            try:
                gamertags = gamertag_result.where(DiscordName.discord_name == user.discord_name).get()
                print (gamertags.steam)
            except DiscordName.DoesNotExist:
                print ("Found no gamertags for " + user.discord_name)

        except DiscordName.DoesNotExist:
            print ("Did not find " + dn)

        db.close()


gt = GamerTag()
gt.add_gamertag()
#gt.list_gamertag()
