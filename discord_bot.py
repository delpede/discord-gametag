#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
A gamertag Discord Bot
https://github.com/Rapptz/discord.py
"""

import logging
import yaml
import discord
import asyncio
import requests
from peewee import *

# Bot specific config
with open('botconfig.yml') as ymlfile:
    botconfig = yaml.load(ymlfile)

db = SqliteDatabase(botconfig['discordbot']['database'])

botclienttoken = botconfig['discordbot']['clienttoken']
client = discord.Client(command_prefix="!")

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logfilename = botconfig['logging']['logpath'] + botconfig['logging']['logname']
handler = logging.FileHandler(logfilename)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s -\
 %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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

        db.get_conn()
        result = DiscordName.select().where(DiscordName.discord_name == dn)

        try:
            user = result.where(DiscordName.discord_name == dn).get()
            print("Found user " + user.discord_name)

        except DiscordName.DoesNotExist:
            print("Did not find " + dn)
            logger.error("Did not find {dn}".format(dn=dn))
            return 1

        db.close()

    def add_gamertag(self, dn, gp, gt):

        try:

            db.get_conn()

            result = DiscordName.select().\
                where(DiscordName.discord_name.contains(dn))
            user = result.where(DiscordName.discord_name.contains(dn)).\
                get()

            if result is not None:
                if gp.lower() == "steam":
                    update = DiscordName.update(steam=gt).\
                        where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "origin":
                    update = DiscordName.update(origin=gt).\
                        where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "battlenet":
                    update = DiscordName.update(battlenet=gt).\
                        where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                elif gp.lower() == "uplay":
                    update = DiscordName.update(uplay=gt).\
                        where(DiscordName.discord_name == user.discord_name)
                    update.execute()
                else:
                    return "Invalid gameplatform"

            else:

                if gp.lower() == "steam":
                    DiscordName.create(discord_name=dn, steam=gt)
                elif gp.lower() == "origin":
                    DiscordName.create(discord_name=dn, origin=gt)
                elif gp.lower() == "battlenet":
                    DiscordName.create(discord_name=dn, battlenet=gt)
                elif gp.lower() == "uplay":
                    DiscordName.create(discord_name=dn, uplay=gt)

            return "Added gamer tag {gt} on {gp} for user {dn}"\
                .format(gt=gt, gp=gp, dn=dn)

        except Exception as e:
            print(e)
            logger.exception("Could not add Gamertag: " + e)
        db.close()

    def list_gamertag(self, dn):

        db.get_conn()
        result = DiscordName.select().where(DiscordName.discord_name.contains(dn))

        try:
            user = result.where(DiscordName.discord_name.contains(dn)).get()

            gamertag_result = DiscordName.select(
                DiscordName.steam,
                DiscordName.origin,
                DiscordName.uplay,
                DiscordName.battlenet).\
                where(DiscordName.discord_name == user.discord_name)

            gamertags = gamertag_result.where(DiscordName.discord_name == user.discord_name).get()

            return gamertags.steam, gamertags.origin, gamertags.uplay, gamertags.battlenet

        except DoesNotExist as e:
            print(e)
            logger.exception("Did not find any gamertags for user {dn}: {error}".format(dn=dn, error=e))
            return "Did not find any gamertags for user {}".format(dn)

        finally:
            db.close()


class BotCommands:

    def rand_cat():
        try:
            # get cat
            cat_params = {'format': 'src'}
            cat_url = 'http://thecatapi.com/api/images/get'
            resp = requests.get(cat_url, params=cat_params)

            return resp.url

        except requests.HTTPError as e:
            print("This failed {}".format(e))
            logger.exception("rand_cat failed with error: {e}".format(e))


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

    elif message.content.startswith('!cat'):
        msg = BotCommands.rand_cat()
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
    logger.exception(e)
