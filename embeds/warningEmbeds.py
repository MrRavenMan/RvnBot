from discord import Embed, Colour

from datetime import datetime


class WarningEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.colour = Colour.from_rgb(255, 175, 0)        

class UserWarningEmbed(WarningEmbed):
    def __init__(self, user, offense, description, channel):
        super().__init__()
        self.title = "**USER WARNING**"
        self.user = user
        self.offense = offense
        self.channel = channel
        self.reaction = "No reaction"

        self.add_field(name="User:", value=f"{user.mention}", inline=True)
        self.add_field(name="Channel:", value=channel.mention, inline=True)
        self.add_field(name="Offense:", value=offense, inline=False)
        self.add_field(name="Description:", value=description, inline=False)
        

    def add_reaction(self, reaction):
        self.reaction = reaction
        self.add_field(name="Reaction:", value=reaction, inline=False)


    def print_warning_to_console(self):
        print("------------------- USER WARNING --------------------------")
        print(f"{self.user.name}#{self.user.discriminator} has committed offense: {self.offense} \n \
            in channel {self.channel.name} \n Description: {self.description} \n Reaction: {self.reaction} \n \
                At time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        print("---------------------------------------------")