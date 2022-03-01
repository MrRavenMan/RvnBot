import configparser

import discord
from discord.ui import InputText, Modal

from views.roleButtonView import RoleAssignmentView

config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class RoleDropdown(discord.ui.Select):
        def __init__(self, roles):
            options = []
            self.roles = roles
            for idx, role in enumerate(self.roles):
                    options.append(discord.SelectOption(label=role.name, description="Make assignment buttons for this role", value=idx))
            super().__init__(
                placeholder="Choose role for assignment button...",
                min_values=1,
                max_values=1,
                options=options,
            )
        
        async def callback(self, interaction: discord.Interaction):
            modal = RoleAssignButtonModal(roles=self.roles[int(self.values[0])])
            await interaction.response.send_modal(modal)


class RoleAssignButtonModal(Modal):
        def __init__(self, roles) -> None:
            super().__init__("Button description")
            self.roles = roles
            self.description = "**This role is for {role_mention} of the community {faq_channel}**"
            self.assign_btn_label = "Assign Role"
            self.unassign_btn_label = "Unassign Role"
            
            self.add_item(InputText(label="Button description", placeholder=self.description, style=discord.InputTextStyle.long, required=False))
            self.add_item(InputText(label="Assign button text", placeholder=self.assign_btn_label, required=False))
            self.add_item(InputText(label="Unassign button text", placeholder=self.unassign_btn_label, required=False))

        async def callback(self, interaction: discord.Interaction):
            role = self.roles
            if self.children[0].value is not None:
                self.description = self.children[0].value
            if self.children[1].value is not None:
                self.assign_btn_label = self.children[1].value
            if self.children[2].value is not None:
                self.unassign_btn_label = self.children[2].value
            
            print(f'Adding button for {role.name}')
            view = RoleAssignmentView(role, assign_btn_label=self.assign_btn_label, unassign_btn_label=self.unassign_btn_label)
        
            await interaction.channel.send(
                    content=self.description.format(role_mention=role.mention,
                        faq_channel=interaction.guild.get_channel(int(config["Assigner"]["faq_channel_id"])).mention),
                    view=view
                )
            await interaction.response.send_message("Buttons generated...", delete_after=3)


class RoleButtonSetupView(discord.ui.View):
        def __init__(self, roles):
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(RoleDropdown(roles))