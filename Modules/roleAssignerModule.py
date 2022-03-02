import configparser
import json

import discord
from discord import Member, Option, Role
from discord.ext import commands

from helpers.command_helpers import cmd_acknowledge
from views.roleButtonView import RoleAssignmentView
from views.roleButtonSetupView import RoleAssignButtonModal
from views.roleAssignerDropdownView import RoleAssignerView

config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class Assigner(commands.Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config
        self.btns_on = True # If true, buttons are already activated
        self.assigner_roles = []
    
    async def load_assigner_roles(self):
        with open('config/assigner_roles.json') as assigner_roles_file:
            self.assigner_roles = json.load(assigner_roles_file)


    def listen_for_butttons(self):  # Goes through all assignable roles and listens 
        for guild in self.bot.guilds: # for role assignment button clicks for each role
            for role in guild.roles:
                if role.is_assignable():
                    self.bot.add_view(RoleAssignmentView(role))


    @commands.Cog.listener()  
    async def on_ready(self): # Function that runs on startup
        print("Assigner: ONLINE")

        await self.load_assigner_roles()
        self.listen_for_butttons()


    """ Commands for special roles """
    @commands.has_role(owner)
    @commands.slash_command(name="assign", brief="Assign role to user")
    async def assign(self, ctx, user: Option(Member, description="Member to assign role to", required=True)):
        for assigner_role in self.assigner_roles:
            if ctx.guild.get_role(int(assigner_role["assigner_role_id"])) in ctx.user.roles:
                roles = []
                for role_id in assigner_role["role_ids"]:
                    roles.append(ctx.guild.get_role(int(role_id)))

        view = RoleAssignerView(roles, user)
        await ctx.interaction.response.send_message(content=f"Pick role for {user.mention}:", view=view, delete_after=10)

    
    @commands.has_role(owner)
    @commands.slash_command(name="unassign", brief="Unassign role to user")
    async def unassign(self, ctx, user: Option(Member, description="Member to unassign role", required=True)):
        for assigner_role in self.assigner_roles:
            if ctx.guild.get_role(int(assigner_role["assigner_role_id"])) in ctx.user.roles:
                roles = []
                for role_id in assigner_role["role_ids"]:
                    role = ctx.guild.get_role(int(role_id))
                    if role in user.roles:
                        roles.append(role)

        view = RoleAssignerView(roles, user)
        await ctx.interaction.response.send_message(content="Pick role to remove from user:", view=view, delete_after=10)


    commands.has_role(owner)
    @commands.slash_command(name="role", brief="Add buttons to assign/unassign role")
    async def role(self, ctx, role: Option(discord.Role, description="Role to generate assign/unassign buttons for", required=True)):
        modal = RoleAssignButtonModal(role=role)
        await ctx.interaction.response.send_modal(modal=modal)

