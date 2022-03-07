from discord import Embed, Colour

from datetime import datetime


class InfoEmbed(Embed):
    def __init__(self):
        super().__init__()
        self.colour = Colour.from_rgb(0, 100, 255)


class BotStatusEmbed(InfoEmbed):
    def __init__(self, description):
        super().__init__()
        self.title = "Bot Info"
        self.description = description
        self.set_footer(text="This message wil auto-delete after 10 seconds")


class JoinEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = ""
        self.user = user
        self.description = f"{self.user.mention} has joined the server."
        self.colour = Colour.from_rgb(0, 204, 68)


class LeaveEmbed(InfoEmbed):
    def __init__(self, user):
        super().__init__()
        self.title = ""
        self.user = user
        self.description = f"{self.user.mention} has left the server."
        self.colour = Colour.from_rgb(255, 0, 0)


class RoleEmbed(InfoEmbed):
    def __init__(self, user, role, unassign=False, print_to_console=True):
        super().__init__()
        self.title = ""
        self.user = user
        self.role = role
        self.unassigned = unassign
        if unassign:
            self.description = f"{self.user.mention} has been unassigned the role {role.mention}."
            if print_to_console:
                print("------------------- USER INFO --------------------------")
                print(f"{self.user.name}#{self.user.discriminator} has been unassigned role: {role.name} \
                        At time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
                print("---------------------------------------------")
        else:
            self.description = f"{self.user.mention} has been assigned the role {role.mention}"
            if print_to_console:
                print("------------------- USER INFO --------------------------")
                print(f"{self.user.name}#{self.user.discriminator} has been assigned role: {role.name} \
                        At time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
                print("---------------------------------------------")