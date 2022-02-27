import configparser
import discord

from discord.ext.commands import Cog, command, has_role

from ..helpers.status import set_status

config = configparser.ConfigParser()
config.read("conf/config.ini")
owner = config["General"]["manager_role"]


class General(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config    


    @Cog.listener()
    async def on_ready(self):
        print("General Module: ONLINE")

        set_status(client=self.client, status=self.config["status"], status_msg=self.config["status_message"], 
                        status_streaming_url=self.config["status_streaming_url"])
        print(f'{self.config["bot_name"]} has logged in as {self.client.user}') # Display online in console


    """ Utility commands """
    @command(brief="Test if bot is online")  # Command to test if bot is online
    @has_role(config["General"]["manager_role"])
    async def test(self, ctx,):
        await ctx.message.channel.send('I am online :D')
        await ctx.message.delete()

    # @command(brief="Reload all config and description files")  # Command to reload all config and text files
    # @has_role(config["General"]["manager_role"])
    # async def reload(self, ctx):
    #     config.read("conf/config.ini")
    #     self.client.remove_cog("Assigner")
    #     self.client.remove_cog("RoleWatcher")
    #     self.client.add_cog(Assigner(self.client, config['Assigner']))
    #     self.client.add_cog(MemberWatch(self.client, config['MemberWatch']))
    #     await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
    #     time.sleep(0.5)
    #     await ctx.message.delete()
    #     print("Reloading complete")

    @command(aliases=["quit"], brief='Shut down bot')  # Command to shut down the bot
    @has_role(config["General"]["manager_role"])
    async def close(self, ctx):
        await self.client.close()
        print("Bot shutting down")


    @command(brief="Add role")
    @has_role(config["General"]["manager_role"])  # Add role using commmand
    async def add_role(self, ctx, role: discord.Role, user: discord.Member):
        if ctx.author.guild_permissions.administrator:
            await user.add_roles(role)
            await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
            print(f"Successfully given {role.mention} to {user.mention}.")


    @command(brief="Removes role")
    @has_role(config["General"]["manager_role"])  # Remove role using commmand
    async def remove_role(self, ctx, role: discord.Role, user: discord.Member):
        if ctx.author.guild_permissions.administrator:
            await user.remove_roles(role)
            await ctx.send(f"Successfully removed {role.mention} from {user.mention}.")
            print(f"Successfully removed {role.mention} from {user.mention}.")

