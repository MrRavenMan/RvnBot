from discord import ButtonStyle
from discord.ui import Button, View


class PunishButtonsView(View):  # Persistent view for assigning single role with btns
        def __init__(self, bot, offender, message, blacklist_msg_channel_id, warning_embed):
            super().__init__(timeout=None)

            kick_btn = self.kickButton(bot, offender, message, blacklist_msg_channel_id, warning_embed)
            ban_btn = self.banButton(bot, offender, message, blacklist_msg_channel_id, warning_embed)

            self.add_item(kick_btn)
            self.add_item(ban_btn)


        class kickButton(Button):
            def __init__(self, bot, offender, message, blacklist_msg_channel_id, warning_embed):
                super().__init__(label="Kick", style=ButtonStyle.blurple, custom_id=f"{offender.name}#{offender.discriminator}_K")
                self.bot = bot
                self.offender = offender
                self.message = message
                self.blacklist_msg_channel_id = blacklist_msg_channel_id
                self.warning_embed = warning_embed

            async def callback(self, interaction):
                reason = f"{self.offender.name}#{self.offender.discriminator} has been kicked. \
                Reason: Wrote blacklisted word in {self.message.channel.name}. {self.offender.name} said: {self.message.content}"
                await self.message.guild.kick(self.offender, reason=reason)
                self.warning_embed.add_reaction(f"User has been kicked by {interaction.user.mention}")
                await self.bot.get_channel(int(self.blacklist_msg_channel_id)).send(embed=self.warning_embed)
                self.warning_embed.print_warning_to_console()
                await interaction.message.delete()

            async def on_error(self, error, item, interaction):
                await interaction.response.send_message(str(error))


        class banButton(Button):
            def __init__(self, bot, offender, message, blacklist_msg_channel_id, warning_embed):
                super().__init__(label="Ban", style=ButtonStyle.red, custom_id=f"{offender.name}#{offender.discriminator}_B")
                self.bot = bot
                self.offender = offender
                self.message = message
                self.blacklist_msg_channel_id = blacklist_msg_channel_id
                self.warning_embed = warning_embed

            async def callback(self, interaction):
                reason = f"{self.offender.name}#{self.offender.discriminator} has been banned. \
                Reason: Wrote blacklisted word in {self.message.channel.name}. {self.offender.name} said: {self.message.content}"
                await self.message.guild.ban(self.offender, reason=reason)
                self.warning_embed.add_reaction(f"User has been banned by {interaction.user.mention}") 
                await self.bot.get_channel(int(self.blacklist_msg_channel_id)).send(embed=self.warning_embed)
                self.warning_embed.print_warning_to_console()
                await interaction.message.delete()

            async def on_error(self, error, item, interaction):
                await interaction.response.send_message(str(error))
