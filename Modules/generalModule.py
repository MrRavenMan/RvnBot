import random
import json
import configparser
import time

from discord.ext.commands import Cog, command, has_role
from discord_components import DiscordComponents


config = configparser.ConfigParser()
config.read("conf/config.ini")
owner = config["General"]["manager_role"]


class Chatter(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config    


    @Cog.listener()
    async def on_ready(self):
        print("General Module: ONLINE")
        print(f'{config["General"]["bot_name"]} has logged in as {client.user}')

        DiscordComponents(self.client)

        try: # Add custom status
            if (int(config["General"]["status"]) == 1):
                print(f"Using status 1: Playing {config['General']['status_message']}")
                await client.change_presence(activity=discord.Game(name=config["General"]["status_message"]))
            elif (int(config["General"]["status"]) == 2):
                print(f"Using status 2: Streaming {config['General']['status_message']}. Link: {config['General']['status_streaming_url']}")
                await client.change_presence(activity=discord.Streaming(name=config["General"]["status_message"], url=config["General"]["status_streaming_url"]))
            elif (int(config["General"]["status"]) == 3):
                print(f"Using status 3: Watching {config['General']['status_message']}")
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config["General"]["status_message"]))
            elif (int(config["General"]["status"]) == 4):
                print(f"Using status 4: Competing in {config['General']['status_message']}")
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=config["General"]["status_message"]))
            elif (int(config["General"]["status"]) == 5):
                print(f"Using status 5: Listening to {config['General']['status_message']}")
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config["General"]["status_message"]))
        except ValueError:
            print("Error loading status. \n Make sure Status in config is a number. Set status to 0 to turn status off")
        except:
            print("ERROR (Non valueError) loading status")


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

