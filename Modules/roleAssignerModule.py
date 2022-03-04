import json

from discord import Member, Option, Role
from discord.ext.commands import Cog, has_any_role, slash_command

from helpers.config_loader import config, admin
from views.roleButtonView import RoleAssignmentView
from views.roleButtonSetupModal import RoleAssignButtonModal
from views.roleAssignerDropdownView import RoleAssignerView


class Assigner(Cog):
    def __init__(self, client):
        self.bot = client
        self.btns_on = True # If true, buttons are already activated
        self.assigner_roles = []

    @Cog.listener()  
    async def on_ready(self): # Function that runs on startup
        print("Assigner: ONLINE")

        await self.load_assigner_roles()
        self.listen_for_butttons()


    """ Commands for special roles """
    @slash_command(name="assign", description="Assign role to user") # Command to assign a role to a user. Assignable roles are defined in config/assigner_roles.json
    async def assign(self, ctx, user: Option(Member, description="Member to assign role to", required=True)):
        roles = None
        for assigner_role in self.assigner_roles:
            if ctx.guild.get_role(int(assigner_role["assigner_role_id"])) in ctx.user.roles:
                roles = []
                for role_id in assigner_role["role_ids"]:
                    roles.append(ctx.guild.get_role(int(role_id)))
        if roles is not None:
            view = RoleAssignerView(roles, user)
            await ctx.interaction.response.send_message(content=f"Pick role for {user.mention}:", view=view, delete_after=10)
        else:
            await ctx.interaction.response.send_message(content=f"You are not allowed to use this command!", delete_after=5)

    @slash_command(name="unassign", description="Unassign role to user") # Command to unassign a role to a user. Assignable roles are defined in config/assigner_roles.json
    async def unassign(self, ctx, user: Option(Member, description="Member to unassign role", required=True)):
        roles = None
        for assigner_role in self.assigner_roles:
            if ctx.guild.get_role(int(assigner_role["assigner_role_id"])) in ctx.user.roles:
                roles = []
                for role_id in assigner_role["role_ids"]:
                    role = ctx.guild.get_role(int(role_id))
                    if role in user.roles:
                        roles.append(role)

        if roles is not None:
            view = RoleAssignerView(roles, user, unassign=True)
            await ctx.interaction.response.send_message(content="Pick role to remove from user:", view=view, delete_after=10)
        else:
            await ctx.interaction.response.send_message(content=f"You are not allowed to use this command!", delete_after=5)

    @has_any_role(admin, config["Assigner"]["manage_role"])
    @slash_command(name="role", description="Add buttons to assign/unassign role") # Command to spawn role assignment buttons
    async def role(self, ctx, role: Option(Role, description="Role to generate assign/unassign buttons for", required=True)):
        modal = RoleAssignButtonModal(role=role)
        await ctx.interaction.response.send_modal(modal=modal)


    """ Utility commands """
    slash_command(name="assigner_roles", description=f'Reload assignable roles')
    @has_any_role(admin, config["Assigner"]["manage_assigner_roles"])
    async def assigner_roles(self, ctx): # Reload chats command - calls load_chats func
        await self.load_assigner_roles()
        await ctx.interaction.response.send_message(content="Assigner roles reloaded!", delete_after=5)

    @slash_command(name="add_role", description="Add role to user")
    @has_any_role(admin, config["Assigner"]["manage_role_cmd"])  # Add role to user using commmand
    async def add_role(self, ctx, role: Option(Role, description="Role to assign", required=True), user: Option(Member, description="Member to assign role to", required=True)):
        if ctx.author.guild_permissions.administrator:
            await user.add_roles(role)
            await ctx.interaction.response.send_message(content=f"Successfully given {role.mention} to {user.mention}.", delete_after=7)
            print(f"Successfully given {role.name} to {user.name}.")

    @slash_command(name="remove_role", description="Remove role from user")
    @has_any_role(admin, config["Assigner"]["manage_role_cmd"])  # Remove role from user using commmand
    async def remove_role(self, ctx, role: Option(Role, description="Role to assign", required=True), user: Option(Member, description="Member to assign role to", required=True)):
        if ctx.author.guild_permissions.administrator:
            await user.remove_roles(role)
            await ctx.interaction.response.send_message(content=f"Successfully removed {role.mention} from {user.mention}.", delete_after=7)
            print(f"Successfully removed {role.name} from {user.name}.")
        
        
    """ Methods """
    async def load_assigner_roles(self): # Load assigner roles
        with open('config/assigner_roles.json') as assigner_roles_file:
            self.assigner_roles = json.load(assigner_roles_file)
        print("Assignable roles reloaded")


    def listen_for_butttons(self):  # Goes through all assignable roles and listens 
        for guild in self.bot.guilds: # for role assignment button clicks for each role
            for role in guild.roles:
                if role.is_assignable():
                    self.bot.add_view(RoleAssignmentView(role))