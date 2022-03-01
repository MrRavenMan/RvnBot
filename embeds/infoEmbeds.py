from discord import Embed, Colour

from datetime import datetime


class InfoEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.colour = Colour.from_rgb(0, 100, 255)
        self.timestamp = datetime.utcnow()


class JoinEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = "**USER JOINED**"
        self.user = user
        self.description = f"{self.user.mention} has joined the server"


class LeaveEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = "**USER LEFT**"
        self.user = user
        self.description = f"{self.user.mention} has left the server"