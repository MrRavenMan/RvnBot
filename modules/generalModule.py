from discord.ext.commands import Cog, slash_command, has_any_role, command

from helpers.status import set_status
from helpers.command_helpers import cmd_acknowledge
from helpers.config_loader import config, admin

from embeds.infoEmbeds import BotStatusEmbed

from discord_together import DiscordTogether


class General(Cog):
    def __init__(self, client):
        self.bot = client


    @Cog.listener()
    async def on_ready(self):
        print("General Module: ONLINE")

        await set_status(client=self.bot, status=config["General"]["status"], status_msg=config["General"]["status_message"], 
                        status_streaming_url=config["General"]["status_streaming_url"])

        description = f"{self.bot.user} has logged in and is now online!"
        print(description)
        embed = BotStatusEmbed(description=description)
        await self.bot.get_channel(int(config["General"]["bot_info_channel_id"])).send(embed=embed, delete_after=15)

        self.bot.togetherControl = await DiscordTogether("BOT_TOKEN_HERE")
        print('Bot is online!')
    
    @command()
    async def start(self, ctx):
        print("Something worked")
        link = await self.bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")

    """ Utility commands """
    @slash_command(name="test", description="Test if bot is online")  # Command to test if bot is online
    @has_any_role(admin, config["General"]["manage_test"])
    async def test(self, ctx,):
        await ctx.interaction.response.send_message(content=f"I am online!", delete_after=3)

    @slash_command(name="close", description='Shut down bot')  # Command to shut down the bot
    @has_any_role(admin, config["General"]["manage_close"])
    async def close(self, ctx):
        description = f"Shutting bot down."
        print(description)
        embed = BotStatusEmbed(description=description)
        await self.bot.get_channel(int(config["General"]["bot_info_channel_id"])).send(embed=embed, delete_after=10)
        await ctx.interaction.response.send_message(content=description, delete_after=3)
        await self.bot.close()

    @command(aliases=["msg"], brief='Make bot send message in chat')  # Command to shut down the bot
    @has_any_role(admin, config["General"]["manage_msg"])
    async def message(self, ctx):
        msg = ctx.message.content.replace("!msg", "").replace("!message", "")
        if not (msg is None or msg == ""):
            await ctx.send(msg)
        if len(ctx.message.attachments) > 0:
            for i in range(len(ctx.message.attachments)):
                await ctx.send(ctx.message.attachments[i].url)
        await cmd_acknowledge(ctx)