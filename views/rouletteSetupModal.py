import configparser

import discord
from discord.ui import InputText, Modal

from views.rouletteButtonView import RouletteButtonView


config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class RouletteSetupModal(Modal):
        def __init__(self, roulette_options) -> None:
            super().__init__("Button description")
            self.roulette_options = roulette_options
            
            self.description = "**This button will either make you laugh or cry**"
            self.roulette_btn_label = "Play roulette!"
            
            self.add_item(InputText(label="Button description", placeholder=self.description, style=discord.InputTextStyle.long, required=False))
            self.add_item(InputText(label="Roulette button text", placeholder=self.roulette_btn_label, required=False))


        async def callback(self, interaction: discord.Interaction):
            if self.children[0].value is not None:
                self.description = self.children[0].value
            if self.children[1].value is not None:
                self.roulette_btn_label = self.children[1].value
            
            print(f'Adding roulette button')
            view = RouletteButtonView(roulette_options=self.roulette_options, roulette_btn_label=self.roulette_btn_label)
            await interaction.channel.send(content=self.description, view=view)

            await interaction.response.send_message("Button generated...", delete_after=1)