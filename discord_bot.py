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
                #print("Found user {} updating {}".format(user.discord_name, gp.lower()))

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
            # For debugging. TODO remove
            print("Found user " + user.discord_name)

            gamertag_result = DiscordName.select(
                DiscordName.steam,
                DiscordName.origin,
                DiscordName.uplay,
                DiscordName.battlenet).where(DiscordName.discord_name == user.discord_name)

            try:
                gamertags = gamertag_result.where(DiscordName.discord_name == user.discord_name).get()

                return gamertags.steam, gamertags.origin, gamertags.uplay, gamertags.battlenet


            except DiscordName.DoesNotExist:
                print("Found no gamertags for " + user.discord_name)

        except DiscordName.DoesNotExist:
            print("Did not find {}".format(dn))

        db.close()


class BotControl:
    """
    Bot control class
    """

    def bot_commands(self):

        gamertag = GamerTag()

        input_command = str(input("->: "))
        command_prefix = "!"

        if input_command[0] == command_prefix:
            if 2 <= len(input_command.split()) <= 4:
                if input_command.split()[0] == "!list":
                    gt = input_command.split()[1]
                    gamertag.list_gamertag(gt)

                elif input_command.split()[0] == "!add":
                    dn = input_command.split()[1]
                    gp = input_command.split()[2]
                    gt = input_command.split()[3]
                    gamertag.add_gamertag(dn, gp, gt)

                else:
                    self.bot_commands()

            else:
                if len(input_command.split()) < 2:
                    print("To few arguments")
                    return self.bot_commands()

                elif len(input_command.split()) > 4:
                    print("To many arguments")
                    return self.bot_commands()

                else:
                    return self.bot_commands()

        else:
            return self.bot_commands()


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
        listinput = message.content.split()[1:]
        dn = ' '.join(listinput)
        
        msg = gamertag.list_gamertag(dn)
        fixedmsg = []
        if msg[0] is not None:
            steam = "Steam: {} ".format(msg[0])
            fixedmsg.append(steam)

        if msg[1] is not None:
            origin = "Origin: {} ".format(msg[1])
            fixedmsg.append(origin)

        if msg[2] is not None:
            uplay = "uPlay: {} ".format(msg[2])
            fixedmsg.append(uplay)

        if msg[3] is not None:
            battlenet = "Battlenet: {} ".format(msg[3])
            fixedmsg.append(battlenet)

        joinedmsg = ''.join(fixedmsg)
        await client.send_message(message.channel, joinedmsg)

    elif message.content.startswith('!add'):
        dn = message.author
        gp = message.content.split()[1]
        gt = message.content.split()[2]
        msg = gamertag.add_gamertag(dn, gp, gt)
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


