from discord import ButtonStyle
from discord.ui import Button, View

from helpers.role_assignment import assign, unassign, invert


class RoleAssignmentView(View):  # Persistent view for assigning single role with btns
        def __init__(self, role, assign_btn_label = "Assign Role", unassign_btn_label = "Unassign Role"):
            super().__init__(timeout=None)

            join_btn = self.JoinRoleButton(role, assign_btn_label)
            leave_btn = self.LeaveRoleButton(role, unassign_btn_label)

            self.add_item(join_btn)
            self.add_item(leave_btn)


        class JoinRoleButton(Button):
            def __init__(self, role, assign_btn_label):
                id = f"J{str(role.id)}"
                super().__init__(label=assign_btn_label, style=ButtonStyle.green, custom_id=id)
                self.role = role

            async def callback(self, interaction):
                await assign(interaction, self.role)

            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))


        class LeaveRoleButton(Button):
            def __init__(self, role, unassign_btn_label):
                id = f"L{str(role.id)}"
                super().__init__(label=unassign_btn_label, style=ButtonStyle.red,  custom_id=id)
                self.role = role

            async def callback(self, interaction):
                await unassign(interaction, self.role)
            
            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))


class MultiRoleAssignmentView(View):  # Persistent view for assigning multiple roles with btns
        def __init__(self, roles):
            super().__init__(timeout=None)
            
            join_btn = self.JoinRolesButton(roles)
            leave_btn = self.LeaveRolesButton(roles)

            self.add_item(join_btn)
            self.add_item(leave_btn)


        class JoinRolesButton(Button):
            def __init__(self, roles):
                id = f"J_ALL"
                super().__init__(label="Assign All Roles", style=ButtonStyle.green, custom_id=id)
                self.roles = roles

            async def callback(self, interaction):
                for role in self.roles:
                    await assign(interaction, role)

            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))


        class LeaveRolesButton(Button):
            def __init__(self, roles):
                id = f"L_ALL"
                super().__init__(label="Unassign All Roles", style=ButtonStyle.red,  custom_id=id)
                self.roles = roles

            async def callback(self, interaction):
                for role in self.roles:
                    await unassign(interaction, role)
            
            async def on_error(self, error, item, interaction):
                await interaction.response.send_msg(str(error))