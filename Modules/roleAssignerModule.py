import configparser
import asyncio

from discord import Member
from discord.ext import commands

from helpers.command_helpers import cmd_acknowledge
from views.roleButtonView import RoleAssignmentView, MultiRoleAssignmentView
from views.roleButtonSetupView import RoleButtonSetupView


config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class Assigner(commands.Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config
        self.btns_on = True # If true, buttons are already activated


    def listen_for_butttons(self):  # Goes through all assignable roles and listens 
        for guild in self.bot.guilds: # for role assignment button clicks for each role
            for role in guild.roles:
                print(role.id, role.name, role.is_assignable())
                if role.is_assignable():
                    self.bot.add_view(RoleAssignmentView(role))


    @commands.Cog.listener()  
    async def on_ready(self): # Function that runs on startup
        print("Assigner: ONLINE")

        self.listen_for_butttons()


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


    @commands.slash_command(guild_ids=[947106474235158548], name="roles")
    async def roles(self, ctx):
        roles = []
        for role in ctx.guild.roles:
            if role.is_assignable():
                roles.append(role)
        view = RoleButtonSetupView(roles)
        
        await ctx.respond("Pick role for role assignment buttons:", view=view, delete_after=10)


    @commands.command(brief=f'Buttons for assigning/unassigning all roles with one click')
    @commands.has_role(owner) # WORK IN PROGRESS
    async def role_all(self, ctx):  # Button for picking all roles with one click
        roles = []
        cmd_input = ctx.message.content.replace("!role_all", "").replace("<@&", "").replace(">", "") # Clean input to a list of role ids
        for id in cmd_input.split():
            if id.isdigit():
                roles.append(ctx.guild.get_role(int(id)))

        print(f'Adding role assignment button for All')
        view = MultiRoleAssignmentView(roles)
    
        with open ("config/roleAssignerConfig/role_all.txt", "r") as myfile:
            data=myfile.readlines()
        role_all_msg = ""
        for i in data:
            role_all_msg += i
        await ctx.send(
            role_all_msg.format(faq_channel=ctx.guild.get_channel(int(self.config["faq_channel_id"])).mention),
            view=view
        )

        await cmd_acknowledge(ctx)

