import json
import time
import configparser
import asyncio

import discord
from discord import Member, ButtonStyle
from discord.ext import commands
from discord import utils, Embed, Colour, File, Forbidden
#from discord_components import Button, ButtonStyle, InteractionType, component
from discord.ui import Button, View

from helpers.command_helpers import cmd_acknowledge
from helpers.role_assignment import assign, unassign, invert

config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]



class Assigner(commands.Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config
        self.btns_on = True # If true, buttons are already activated

        with open('config/roleAssignerConfig/roles.json') as json_file:
            self.roles = json.load(json_file)

        with open ("config/roleAssignerConfig/role_btn_msg.txt", "r") as myfile:
            data=myfile.readlines()
        self.role_btn_msg = ""
        for i in data:
            self.role_btn_msg += i


    @commands.Cog.listener()  
    async def on_ready(self): # Function that runs on startup
        print("Assigner: ONLINE")

        self.listen_for_butttons()

    @commands.command(brief=f'Buttons for assigning/unassigning all roles with one click')
    @commands.has_role(owner)
    async def role_all(self, ctx):  # Button for picking all roles with one click
        join = Button(style=ButtonStyle.blue, label="Assign All Roles", id="e_all_join")
        leave = Button(style=ButtonStyle.red, label="Unassign All Roles", id="e_all_leave")

        with open ("conf/Assigner_conf/role_all.txt", "r") as myfile:
            data=myfile.readlines()
        role_all_msg = ""
        for i in data:
            role_all_msg += i

        await ctx.send(
            role_all_msg.format(faq_channel=ctx.guild.get_channel(int(self.config["faq_channel_id"])).mention),
            components=[
                [join, leave]
            ]
        )
        await cmd_acknowledge(ctx)


    """ Commands for special roles """
    try:
        if int(config["Assigner"]["special_role_1_admin_id"]) != 0 and int(config["Assigner"]["special_role_1_id"]) != 0:
            @commands.command(brief=f'Add/Remove Special role 1 to <UserTagged>')
            @commands.has_any_role(owner, int(config["Assigner"]["special_role_1_admin_id"]))
            async def special_role1(self, ctx, user: Member): # Display available role commands
                role = ctx.guild.get_role(int(self.config["special_role_1_id"]))
                if role not in user.roles:
                    await user.add_roles(role)
                    print(f"{user.name} has been assigned the role of {role.name}")
                elif role in user.roles:
                    await user.remove_roles(role)
                    print(f"{user.name} has been unassigned the role of {role.name}")
                else:
                    print(f"An error orcurred while trying to invert {role.name}'s special role 1 role")

                await cmd_acknowledge(ctx)
    except ValueError:
        print("Please make sure special_role_1_admin_id and special_role_1_id is a role ID or 0 to disable")
    except:
        print("Error loading special role 1 or/and special role 1 admin")

    try:
        if int(config["Assigner"]["special_role_2_admin_id"]) != 0 and int(config["Assigner"]["special_role_2_id"]) != 0:
            @commands.command(brief=f'Add/Remove Special role 2 to <UserTagged>')
            @commands.has_any_role(owner, int(config["Assigner"]["special_role_2_admin_id"]))
            async def special_role2(self, ctx, user: Member): # Display available role commands
                role = ctx.guild.get_role(int(self.config["special_role_2_id"]))
                if role not in user.roles:
                    await user.add_roles(role)
                    print(f"{user.name} has been assigned the role of {role.name}")
                elif role in user.roles:
                    await user.remove_roles(role)
                    print(f"{user.name} has been unassigned the role of {role.name}")
                else:
                    print(f"An error orcurred while trying to invert {role.name}'s special role 2 role")

                await cmd_acknowledge(ctx)
    except ValueError:
        print("Please make sure special_role_2_admin_id and special_role_2_id is a role ID or 0 to disable")
    except:
        print("Error loading special role 2 or/and special role 2 admin")

    try:
        if int(config["Assigner"]["special_role_3_admin_id"]) != 0 and int(config["Assigner"]["special_role_3_id"]) != 0:
            @commands.command(brief=f'Add/Remove Special role 3 to <UserTagged>')
            @commands.has_any_role(owner, int(config["Assigner"]["special_role_3_admin_id"]))
            async def special_role3(self, ctx, user: Member): # Display available role commands
                role = ctx.guild.get_role(int(self.config["special_role_3_id"]))
                if role not in user.roles:
                    await user.add_roles(role)
                    print(f"{user.name} has been assigned the role of {role.name}")
                elif role in user.roles:
                    await user.remove_roles(role)
                    print(f"{user.name} has been unassigned the role of {role.name}")
                else:
                    print(f"An error orcurred while trying to invert {role.name}'s special role 3 role")

                await cmd_acknowledge(ctx)
    except ValueError:
        print("Please make sure special_role_3_admin_id and special_role_3_id is a role ID or 0 to disable")
    except:
        print("Error loading special role 3 or/and special role 3 admin")

    def listen_for_butttons(self):
        for guild in self.bot.guilds:
            for role in guild.roles:
                print(role.id, role.name, role.is_assignable())
                if role.is_assignable():
                    self.bot.add_view(self.PersistentView(role))


    @commands.command(brief=f'Buttons for assigning/unassigning Role 1')
    @commands.has_role(owner)
    async def role(self, ctx):
        role_id = int(ctx.message.content.replace("!role", "").replace("<@&", "").replace(">", ""))
        role = ctx.guild.get_role(role_id)
        await self.role_func(ctx, role)


    class PersistentView(View):
        def __init__(self, role):
            super().__init__(timeout=None)
            
            join_btn = self.JoinRoleButton(role)
            leave_btn = self.LeaveRoleButton(role)

            self.add_item(join_btn)
            self.add_item(leave_btn)


        class JoinRoleButton(Button):
            def __init__(self, role):
                id = f"J{str(role.id)}"
                print(id)
                super().__init__(label="Assign role", style=ButtonStyle.green, custom_id=id)
                self.role = role

            async def callback(self, interaction):
                await assign(interaction, self.role)

            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))


        class LeaveRoleButton(Button):
            def __init__(self, role):
                id = f"L{str(role.id)}"
                print(id)
                super().__init__(label="Unassign role", style=ButtonStyle.red,  custom_id=id)
                self.role = role

            async def callback(self, interaction):
                await unassign(interaction, self.role)
            
            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))

    
    async def role_func(self, ctx, role):
        print(f'Adding button for {role.name}')
        view = self.PersistentView(role)
    
        if self.config.getboolean("role_btn_tag_later") is True: # Avoids the mention of a role, tagging the whole role
            msg = await ctx.send("Generating button, please hold...")
            await asyncio.sleep(0.7)

            await msg.edit(
                content=self.role_btn_msg.format(role_mention=role.mention,
                                        faq_channel=ctx.guild.get_channel(int(self.config["faq_channel_id"])).mention),
                view=view
                
            )
            await ctx.message.delete()
        elif self.config.getboolean("role_btn_tag_later") is False:
            await ctx.send(
                content=self.role_btn_msg.format(role_mention=role.mention,
                                        faq_channel="FIX THIS"),
                view=view
            )
        else:
            print("ATTENTION: ERROR: Config [Assigner]role_btn_tag_later is invalid. Must be set to True/False!")
        
        
        await ctx.message.delete() # Delete command msg