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
        else:
            print ("Bot added " + gamer_tag + " as " + discord_name + " "+ game_platform + " account")

        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("INSERT INTO gamertags (DISCORD_NAME, {gp}) VALUES (\"{dn}\", \"{gt}\")".format(gp=game_platform, dn=discord_name, gt=gamer_tag))
        except sqlite3.IntegrityError as e:
            print (e)
        finally:
            conn.commit()
            conn.close()


gt = GamerTag()

gt.add_gamertag()
