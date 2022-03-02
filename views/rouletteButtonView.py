from discord import ButtonStyle
from discord.ui import Button, View

from random import choice
from datetime import datetime, timedelta

class RouletteButtonView(View):  # Non-Persistent view for the roulette button
        def __init__(self, roulette_options, roulette_btn_label = "Play roulette!"):
            super().__init__()
            
            roulette_btn = self.RouletteButton(roulette_options, roulette_btn_label)
            self.add_item(roulette_btn)


        class RouletteButton(Button):
            def __init__(self, roulette_options, roulette_btn_label):
                super().__init__(label=roulette_btn_label, style=ButtonStyle.primary)
                self.roulette_options = roulette_options

            async def callback(self, interaction):
                action = choice(self.roulette_options) # select random roulette option

                if action["response"] != "":
                    await interaction.channel.send(content=f"{interaction.user.mention} {action['response']}")

                if int(action["timeout"]) != 0:
                    delta = timedelta(minutes=int(action["timeout"]))
                    reason = f"{interaction.user.name}#{interaction.user.discriminator} has gotten timeout until {(datetime.utcnow() + delta).strftime('%Y-%m-%d %H:%M:%S')}. \
                        Reason: Got unlucky in roulette"
                    await interaction.user.timeout_for(duration=delta, reason=reason)


            async def on_error(self, error, item, interaction):
                await interaction.response.send_message(str(error))