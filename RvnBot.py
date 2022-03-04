import discord

from helpers.config_loader import config
from discord.ext import commands


def main():
    intents = discord.Intents.default()
    intents.members = True

    TOKEN = config["General"]["TOKEN"]

    client = commands.Bot(command_prefix='!', intents=intents)

    """ Load modules """
    # Start modules as specified in config
    from modules.generalModule import General
    client.add_cog(General(client))

    if config.getboolean("General", "enable_Assigner"):
        from modules.roleAssignerModule import Assigner
        client.add_cog(Assigner(client))
    else:
        print("Assigner: OFF - not enabled in config")

    if config.getboolean("General", "enable_MemberWatch"):
        from modules.memberWatchModule import MemberWatch
        client.add_cog(MemberWatch(client))
    else:
        print("Member Watch: OFF - not enabled in config")

    if config.getboolean("General", "enable_Chatter"):
        from modules.chatterModule import Chatter
        client.add_cog(Chatter(client))
    else:
        print("Chatter: OFF - not enabled in config")


    client.run(TOKEN)


""" RUN """
if __name__ == "__main__":
    main()

