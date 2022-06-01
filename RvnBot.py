import discord
from discord.ext.commands.errors import MissingAnyRole, CommandNotFound

from helpers.config_loader import config
from discord.ext import commands

from discord_together import DiscordTogether


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

    @client.event
    async def on_application_command_error(ctx, error):
        if isinstance(error, MissingAnyRole):
            pass # SUPRESS ALL MissingAnyRole errors caused by users not allowed to use commands using slash commands
        if isinstance(error, CommandNotFound):
            pass # SUPRESS ALL CommandNotFound errors caused by users using ! command not existing within RavenBot
    client.run(TOKEN)

    @client.event
    async def on_ready():
        client.togetherControl = await DiscordTogether("BOT_TOKEN_HERE")
        print('Bot is online!')

    @client.command()
    async def start(ctx):
        link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")



""" RUN """
if __name__ == "__main__":
    main()

