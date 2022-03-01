from discord import ButtonStyle
from discord.ui import Button, View

from helpers.role_assignment import assign, unassign, invert


class RoleAssignmentView(View):  # Persistent view
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