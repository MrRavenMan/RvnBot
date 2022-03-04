import discord

from views.roleButtonView import RoleAssignmentView
from helpers.role_assignment import assign, unassign


class RoleAssignerDropdown(discord.ui.Select):
    def __init__(self, roles, user, unassign):
        options = []
        self.roles = roles
        self.user = user
        self.unassign = unassign
        for idx, role in enumerate(self.roles):
                options.append(discord.SelectOption(label=role.name, description="Assign/Unassign user this role", value=idx))
        super().__init__(
            placeholder="Choose role for assignment button...",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.unassign:
            await unassign(self.user, self.roles[int(self.values[0])])
            await interaction.response.send_message(f"Unassigned {self.roles[int(self.values[0])].mention} from {self.user.mention}")
        else:
            await assign(self.user, self.roles[int(self.values[0])])
            await interaction.response.send_message(f"Assigned {self.roles[int(self.values[0])].mention} to {self.user.mention}")


class RoleAssignerView(discord.ui.View):
        def __init__(self, roles, user, unassign=False):
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(RoleAssignerDropdown(roles, user, unassign))