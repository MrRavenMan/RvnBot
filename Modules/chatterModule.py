import random
import json
import configparser
import time

from discord.ext.commands import Cog, command, has_role


config = configparser.ConfigParser()
config.read("config/config.ini")
owner = config["General"]["manager_role"]


class Chatter(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config

        self.calls = []
        self.calls_map = []
        self.always_respond_to_role_ids = []
        self.chats = []
        self.load_chats()
    

    def load_chats(self):
        # Clear class vars
        self.calls = []
        self.calls_map = []

        # load chats.json file
        with open('config/chats.json') as chats_file:
            chats_data = json.load(chats_file)
            self.chats = chats_data["chats"]
            self.always_respond_to_role_ids = chats_data["always_respond_to_role_ids"]

        # map chat calls to index of chats
        for i, chat in enumerate(self.chats):
            for call in chat["call"]:
                self.calls.append(call.lower())
                self.calls_map.append(i)


    @Cog.listener()
    async def on_ready(self):
        print("Chatter Module: ONLINE")
        print(f"Chatter contains {len(self.chats)} different chats")


    @command(brief=f'Reload chats')
    @has_role(owner)
    async def reload_chats(self, ctx): # Display available role commands
        self.load_chats()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        time.sleep(0.5)
        await ctx.message.delete()
        print("Chatter: RELOADED")
        print(f"Chatter contains {len(self.chats)} different chats")


    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user: # Ignore message if by bot itself
            return
        messageAuthor = message.author

        if message.content.lower() in self.calls:
            idx = self.calls.index(message.content.lower())
            chat_idx = self.calls_map[idx]
            
            # If always respond is disabled and user not in specified role, only respond if probability True
            if self.config["always_respond"] == "False" and not any(role.id in self.always_respond_to_role_ids for role in messageAuthor.roles): 
                i = random.uniform(0, 1) 
                k = float(self.chats[chat_idx]["probability"])
                if i > k:
                    return
                
            response = random.choice(self.chats[chat_idx]["response"])
            if "min" in self.chats[chat_idx] and "max" in self.chats[chat_idx]:
                _min = self.chats[chat_idx]["min"]
                _max = self.chats[chat_idx]["max"]
                result = random.randint(_min, _max)
            else:
                _min = 0
                _max = 0
                result = 0


            await message.channel.send(response.format(user_mention=messageAuthor.name,
                                            server_mention=messageAuthor.guild.name,
                                            min=_min, max=_max, result=result))
