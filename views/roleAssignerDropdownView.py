import configparser

import discord
from discord.ui import InputText, Modal

from views.roleButtonView import RoleAssignmentView
from helpers.role_assignment import assign, unassign


config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class RoleAssignerDropdown(discord.ui.Select):
    def __init__(self, roles, user):
        options = []
        self.roles = roles
        self.user = user
        for idx, role in enumerate(self.roles):
                options.append(discord.SelectOption(label=role.name, description="Assign/Unassign user this role", value=idx))
        super().__init__(
            placeholder="Choose role for assignment button...",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        await assign(self.user, self.roles[int(self.values[0])])
        await interaction.response.send_message(f"Assigned {self.roles[int(self.values[0])].mention} to {self.user.mention}")


class RoleAssignerView(discord.ui.View):
        def __init__(self, roles, user):
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(RoleAssignerDropdown(roles, user))