import configparser

import discord
from discord.ui import InputText, Modal

from views.roleButtonView import RoleAssignmentView


config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class RoleAssignButtonModal(Modal):
        def __init__(self, role) -> None:
            super().__init__("Button description")
            self.role = role
            
            self.description = "**This role is for {role_mention} of the community**"
            self.assign_btn_label = "Assign Role"
            self.unassign_btn_label = "Unassign Role"
            
            self.add_item(InputText(label="Button description", placeholder=self.description, style=discord.InputTextStyle.long, required=False))
            self.add_item(InputText(label="Assign button label", placeholder=self.assign_btn_label, required=False))
            self.add_item(InputText(label="Unassign button label", placeholder=self.unassign_btn_label, required=False))

        async def callback(self, interaction: discord.Interaction):
            role = self.role
            if self.children[0].value is not None:
                self.description = self.children[0].value
            if self.children[1].value is not None:
                self.assign_btn_label = self.children[1].value
            if self.children[2].value is not None:
                self.unassign_btn_label = self.children[2].value
            
            print(f'Adding button for {role.name}')
            view = RoleAssignmentView(role, assign_btn_label=self.assign_btn_label, unassign_btn_label=self.unassign_btn_label)
        
            await interaction.channel.send(
                    content=self.description.format(role_mention=role.mention),
                    view=view
                )
            await interaction.response.send_message("Buttons generated...", delete_after=1)
