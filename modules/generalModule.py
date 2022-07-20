from discord.ext.commands import Cog, slash_command, has_any_role, command
from discord import Option, TextChannel
import random

from helpers.status import set_status
from helpers.command_helpers import cmd_acknowledge
from helpers.config_loader import config, admin

from embeds.infoEmbeds import BotStatusEmbed


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
    

    """ Picker commands"""
    @has_any_role(admin, config["Picker"]["manage_role"])
    @slash_command(name="pick", description="Pick random people who reacted to message") # Command to pick users reacting to msg
    async def pick(self, ctx, msg_id: Option(str, description="Message id of message to pick reacting people from", required=True),
                            winners: Option(int, description="Amount of people to pick", required=True),
                            reaction: Option(str, description="Reaction to pick users from (Only default emojis!). Leave empty to allow all reactions", required=False),
                            channel: Option(TextChannel, description="Channel message with id is written in. Leave empty if same channel as command", required=False)):
        if channel is None:
            msg = await ctx.fetch_message(int(msg_id))
        else:
            msg = await channel.fetch_message(int(msg_id))
        reacters = [] # List of users reacting to msg
        for msg_reaction in msg.reactions:
            if msg_reaction.me is False:
                if reaction is None or msg_reaction.emoji == reaction:
                    async for user in msg_reaction.users():
                        reacters.append(user)


        users = [] # List of users checked for duplicates
        for reaction_user in reacters: # Check for duplicate users (users with multiple reactions)
            duplicate = False
            for user in users:
                if user.id == reaction_user.id:
                    duplicate = True
                    continue
            if duplicate is False:
                users.append(reaction_user)

        if winners > len(users): # If more winners than participants, amount of 
            winners = len(users)     # winners will be set to amount of participants
        winners_list = random.sample(range(0, len(users)), winners)
        response = "Picked:"
        for winner in winners_list:
            response = response + f"\n {users[winner]}"

        await ctx.interaction.response.send_message(response)


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
