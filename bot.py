#!/usr/local/bin/python3

'''
A gamertag Discord Bot
'''

import sqlite3

db = "kompany_bot.db"


class GamerTag():

    def add_gamertag(self):
        try:
            discord_name = str(input("Discord name: "))
            game_platform = input("Game Platform: ")
            gamer_tag = input("Gamer Tag: ")
        except Exception as e:
            print (e)
            return add_gamertag(self)

        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()

            c.execute("SELECT DISCORD_NAME FROM gamertags WHERE DISCORD_NAME = \"{dn}\"".format(dn=discord_name))

            try_discord_name = c.fetchone()
            print (try_discord_name)

            if discord_name in try_discord_name[0]:
                try_discord_name = c.fetchone()
                c.execute("UPDATE gamertags SET \"{gp}\"=\"{gt}\" WHERE DISCORD_NAME = \"{dn}\"".format(gp=game_platform, gt=gamer_tag, dn=discord_name))
                print ("Bot updated " + gamer_tag + " as " + discord_name + " "+ game_platform + " account")
            else:
                try_discord_name = c.fetchone()
                c.execute("INSERT INTO gamertags (DISCORD_NAME, {gp}) VALUES (\"{dn}\", \"{gt}\")".format(gp=game_platform, dn=discord_name, gt=gamer_tag))
                print ("Bot added " + gamer_tag + " as " + discord_name + " "+ game_platform + " account")
        except sqlite3.IntegrityError as e:
            print (e)
        finally:
            conn.commit()
            conn.close()

    def list_discord_names(self):

        conn = sqlite3.connect(db)
        c = conn.cursor()

        c.execute("SELECT DISCORD_NAME FROM gamertags")

        discord_names = c.fetchall()

        for dn in discord_names:
            print (dn[0])

        conn.close()

gt = GamerTag()
gt.add_gamertag()
gt.list_discord_names()
