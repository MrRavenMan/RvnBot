import discord
import configparser
import time

from discord.ext import commands


def main():
    # Load config and create client class
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    intents = discord.Intents.default()
    intents.members = True

    TOKEN = config["General"]["TOKEN"]

    client = commands.Bot(command_prefix='!', intents=intents)

    """ Load modules """
    # Start modules as specified in config
    from modules.generalModule import General
    client.add_cog(General(client, config["General"]))

    if config.getboolean("General", "enable_Assigner"):
        from modules.roleAssignerModule import Assigner
        client.add_cog(Assigner(client, config['Assigner']))
    else:
        print("Assigner: OFF - not enabled in config")

    if config.getboolean("General", "enable_MemberWatch"):
        from modules.memberWatchModule import MemberWatch
        client.add_cog(MemberWatch(client, config['MemberWatch']))
    else:
        print("Member Watch: OFF - not enabled in config")

    if config.getboolean("General", "enable_Chatter"):
        from modules.chatterModule import Chatter
        client.add_cog(Chatter(client, config['Chatter']))
    else:
        print("Chatter: OFF - not enabled in config")

    if config.getboolean("General", "enable_MusicPlayer"):
        from music_player import MusicPlayer
        client.add_cog(MusicPlayer(client))
    else:
        print("Music Player: OFF - not enabled in config")


    client.run(TOKEN)


""" RUN """
if __name__ == "__main__":
    main()

