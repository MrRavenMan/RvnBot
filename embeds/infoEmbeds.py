from discord import Embed, Colour

from datetime import datetime


class InfoEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.colour = Colour.from_rgb(0, 100, 255)

class JoinEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = ""
        self.user = user
        self.description = f"{self.user.mention} has joined the server"
        self.colour = Colour.from_rgb(0, 204, 68)


class LeaveEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = ""
        self.user = user
        self.description = f"{self.user.mention} has left the server"
        self.colour = Colour.from_rgb(255, 0, 0)