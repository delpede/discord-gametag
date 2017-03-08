#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
A gamertag Discord Bot
https://github.com/Rapptz/discord.py
"""

import yaml
import discord
import asyncio
from peewee import *


with open('botconfig.yml') as ymlfile:
    botconfig = yaml.load(ymlfile)

db = SqliteDatabase('discord_bot.db')

botclienttoken = botconfig['discordbot']['clienttoken']
client = discord.Client(command_prefix="!")


class DiscordName(Model):
    id = IntegerField(primary_key=True)
    discord_name = CharField(unique=True)
    steam = CharField(null=True)
    origin = CharField(null=True)
    battlenet = CharField(null=True)
    uplay = CharField(null=True)

    class Meta:
        database = db

    def create_table_discordname(self):
        db.connect()
        db.create_tables([DiscordName])
        db.close()


class GamerTag:
    """
    This class handles everything related to gamertags.
    """

    def check_discord_name(self, dn):

        db.connect()
        result = DiscordName.select().where(DiscordName.discord_name == dn)

        try:
            user = result.where(DiscordName.discord_name == dn).get()
            print("Found user " + user.discord_name)

        except DiscordName.DoesNotExist:
            print("Did not find " + dn)
            return 1

        db.close()

    def add_gamertag(self, dn, gp, gt):

        try:
            try:

                db.connect()

                result = DiscordName.select().where(DiscordName.discord_name.contains(dn))
                user = result.where(DiscordName.discord_name.contains(dn)).get()

                if gp.lower() == "steam":
                    update = DiscordName.update(steam=gt).where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "origin":
                    update = DiscordName.update(origin=gt).where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "battlenet":
                    update = DiscordName.update(battlenet=gt).where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "uplay":
                    update = DiscordName.update(uplay=gt).where(DiscordName.discord_name == user.discord_name)
                    update.execute()

            except DiscordName.DoesNotExist:
                print("Creating")
                if gp.lower() == "steam":
                    DiscordName.create(discord_name=dn, steam=gt)
                elif gp.lower() == "origin":
                    DiscordName.create(discord_name=dn, origin=gt)
                elif gp.lower() == "battlenet":
                    DiscordName.create(discord_name=dn, battlenet=gt)
                elif gp.lower() == "uplay":
                    DiscordName.create(discord_name=dn, uplay=gt)

            return "Added gamer tag {gt} on {gp} for user {dn}".format(gt=gt, gp=gp, dn=dn)

        except Exception as e:
            print(e)
        db.close()

    def list_gamertag(self, dn):

        db.connect()
        result = DiscordName.select().where(DiscordName.discord_name.contains(dn))

        try:
            user = result.where(DiscordName.discord_name.contains(dn)).get()

            gamertag_result = DiscordName.select(
                DiscordName.steam,
                DiscordName.origin,
                DiscordName.uplay,
                DiscordName.battlenet).where(DiscordName.discord_name == user.discord_name)

            gamertags = gamertag_result.where(DiscordName.discord_name == user.discord_name).get()

            return gamertags.steam, gamertags.origin, gamertags.uplay, gamertags.battlenet

        except DoesNotExist as e:
            print(e)
            return "Did not find any gamertags for user {}".format(dn)

        finally:
            db.close()

@client.event
async def on_message(message):

    gamertag = GamerTag()

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!list'):

        if len(message.content.split()) <= 1:
            await client.send_message(message.channel, "To few arguments")
        else:
            listinput = message.content.split()[1:]
            dn = ' '.join(listinput)

            msg = gamertag.list_gamertag(dn)
            fixedmsg = ''

            if "Did not find any gamertags for user" in msg:
                fixedmsg += msg
            else:
                if msg[0] is not None:
                    fixedmsg += "__**Steam:**__ {} ".format(msg[0])

                if msg[1] is not None:
                    fixedmsg += "__**Origin:**__ {} ".format(msg[1])

                if msg[2] is not None:
                    fixedmsg += "__**uPlay:**__ {} ".format(msg[2])

                if msg[3] is not None:
                    fixedmsg += "__**Battlenet:**__ {} ".format(msg[3])

            await client.send_message(message.channel, fixedmsg)

    elif message.content.startswith('!add'):
        dn = message.author
        gp = message.content.split()[1]
        gt = message.content.split()[2]
        msg = gamertag.add_gamertag(dn, gp, gt)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!help'):
        msg = "**!list** - use !list <discord name> for listing gamertags\n" \
              "**!add** - use !add <steam/origin/uplay/battlenet> <gamertag>"
        await client.send_message(message.channel, msg)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


try:
    client.run(str(botclienttoken))
except discord.ClientException as e:
    print(e)


