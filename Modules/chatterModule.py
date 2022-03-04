import random
import json

from discord.ext.commands import Cog, slash_command, has_any_role

from embeds.infoEmbeds import BotStatusEmbed
from views.rouletteSetupModal import RouletteSetupModal
from helpers.config_loader import config, admin


class Chatter(Cog):
    def __init__(self, client):
        self.bot = client

        self.calls = []
        self.calls_map = []
        self.always_respond_to_role_ids = []
        self.chats_ = []
        self.roulette_options = []
        

    @Cog.listener()
    async def on_ready(self):
        await self.load_chats(startup=True)
        await self.load_roulette(startup=True)
        print("Chatter Module: ONLINE")

    @Cog.listener()
    async def on_message(self, message): # Message listener for chatter
        if message.author == self.bot.user: # Ignore message if by bot itself
            return
        messageAuthor = message.author

        if message.content.lower() in self.calls:
            idx = self.calls.index(message.content.lower())
            chat_idx = self.calls_map[idx]
            
            # If always respond is disabled and user not in specified role, only respond if probability True
            if config["Chatter"]["always_respond"] == "False" and not any(role.id in self.always_respond_to_role_ids for role in messageAuthor.roles): 
                i = random.uniform(0, 1) 
                k = float(self.chats_[chat_idx]["probability"])
                if i > k:
                    return
                
            response = random.choice(self.chats_[chat_idx]["response"])
            if "min" in self.chats_[chat_idx] and "max" in self.chats_[chat_idx]:
                _min = self.chats_[chat_idx]["min"]
                _max = self.chats_[chat_idx]["max"]
                result = random.randint(_min, _max)
            else:
                _min = 0
                _max = 0
                result = 0


            await message.channel.send(response.format(user_mention=messageAuthor.name,
                                            server_mention=messageAuthor.guild.name,
                                            min=_min, max=_max, result=result))


    @slash_command(name="chats", description=f'Reload chats')
    @has_any_role(admin, config["Chatter"]["manage_chats"])
    async def chats(self, ctx): # Reload chats command - calls load_chats func
        await self.load_chats()
        await ctx.interaction.response.send_message(content=f"Chats reloaded!", delete_after=5)
        print("Chatter: RELOADED")

    @slash_command(name="roulette_reload", description=f'Reload roulette options')
    @has_any_role(admin, config["Chatter"]["manage_roulette_reload"])
    async def roulette_reload(self, ctx): # Reload roulette options command - calls load_roulette func
        await self.load_roulette()
        await ctx.interaction.response.send_message(content=f"Roulette options reloaded!", delete_after=5)

    @slash_command(name="roulette", description=f'Make roulette button')
    @has_any_role(admin, config["Chatter"]["manage_roulette"])
    async def roulette(self, ctx): # Reload chats command - calls load_chats func
        modal = RouletteSetupModal(roulette_options=self.roulette_options)
        await ctx.interaction.response.send_modal(modal=modal)
    

    async def load_roulette(self, startup=False): # Reload roulette options
        with open('config/roulette.json') as roulette_file:
            self.roulette_options = json.load(roulette_file)

        description = f"New roulette options loaded. Roulette contains {len(self.roulette_options)} options"
        print(description)
        if not startup:
            embed = BotStatusEmbed(description=description)
            await self.bot.get_channel(int(config["General"]["bot_info_channel_id"])).send(embed=embed, delete_after=15)


    async def load_chats(self, startup=False): # Reload chats function
        # Clear class vars
        self.calls = []
        self.calls_map = []

        # load chats_.json file
        with open('config/chats.json') as chats_file:
            chats_data = json.load(chats_file)
            self.chats_ = chats_data["chats"]
            self.always_respond_to_role_ids = chats_data["always_respond_to_role_ids"]

        # map chat calls to index of chats_
        for i, chat in enumerate(self.chats_):
            for call in chat["call"]:
                self.calls.append(call.lower())
                self.calls_map.append(i)

        description = f"New Chats loaded. Chatter contains {len(self.chats_)} chats"
        print(description)
        if not startup:
            embed = BotStatusEmbed(description=description)
            await self.bot.get_channel(int(config["General"]["bot_info_channel_id"])).send(embed=embed, delete_after=15)