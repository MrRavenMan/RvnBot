import discord

from embeds.infoEmbeds import RoleEmbed
from helpers.role_assignment import assign, unassign


class RoleAssignerDropdown(discord.ui.Select):
    def __init__(self, roles, user, author, unassign):
        options = []
        self.roles = roles
        self.user = user
        self.unassign = unassign
        self.author = author
        for idx, role in enumerate(self.roles):
                options.append(discord.SelectOption(label=role.name, description="Assign/Unassign user this role", value=idx))
        super().__init__(
            placeholder="Choose role for assignment button...",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id: # Check if user using selecting role is cmd author
            return
        if self.unassign:
            await unassign(self.user, self.roles[int(self.values[0])])
            embed = RoleEmbed(self.user, self.roles[int(self.values[0])], unassign=True)
            await interaction.response.send_message(embed=embed, delete_after=10)

        else:
            await assign(self.user, self.roles[int(self.values[0])])
            embed = RoleEmbed(self.user, self.roles[int(self.values[0])])
            await interaction.response.send_message(embed=embed, delete_after=10)


class RoleAssignerView(discord.ui.View):
        def __init__(self, roles, user, author, unassign=False):
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(RoleAssignerDropdown(roles, user, author, unassign))