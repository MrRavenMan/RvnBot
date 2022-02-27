from discord import Forbidden
from discord.ext.commands import Cog, MissingPermissions
from discord.channel import DMChannel

import re
import json


class MemberWatch(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config

        with open('config/memberWatchConfig/blacklist.json') as blacklist_file:
            blacklist_data = json.load(blacklist_file)
            dirty_blacklist = blacklist_data["blacklisted_words"]
            self.whitelisted_role_ids = blacklist_data["whitelisted_role_ids"]

        self.blacklist = []
        for word in dirty_blacklist: # Clean blacklist so all words are lowercase str
            self.blacklist.append(str(word.lower().replace("@", "add_")))


    @Cog.listener()
    async def on_ready(self):
        print("Member Watch Module: ONLINE")
        print(f"Blacklist contains {len(self.blacklist)} blacklisted words")
        print(f"{len(self.whitelisted_role_ids)} roles are whitelisted from the blacklist")

    @Cog.listener()
    async def on_member_join(self, member):
        print("member joined")
        await self.bot.get_channel(int(self.config["join_msg_channel_id"])).send(f"{member.mention} has joined the server!")

        try:
            with open ("config/memberWatchConfig/welcome_dm.txt", "r") as myfile:
                data=myfile.readlines()
            text = ""
            for i in data:
                text += i
            await member.send(text.format(user_mention=member.name,
                                            server_mention=member.guild.name))
        except Forbidden:
            pass


    @Cog.listener()
    async def on_member_remove(self, member):
        print("member left")
        await self.bot.get_channel(int(self.config["leave_msg_channel_id"])).send(f"**{member.name}#{member.discriminator}** has left the server!")

    
    def msg_contains_word(self, msg, word):
        msg = msg.replace("@", "add_")
        return re.search(fr'\b({word})\b', msg) is not None # returns True if bad word is in message

    @Cog.listener()
    async def on_message(self, message):
        messageAuthor = message.author

        if messageAuthor != self.bot.user: # check if message is by bot itself or whitelisted role
            if self.blacklist != None and (isinstance(message.channel, DMChannel) == False) and not any(role.id in self.whitelisted_role_ids for role in messageAuthor.roles):
                for bannedWord in self.blacklist:
                    if self.msg_contains_word(message.content.lower(), bannedWord):
                        await message.delete()

                        message.content = message.content.replace("@", "*@*") # Make sure bot doesn't tag everyone when sending admins blacklist msg

                        await self.bot.get_channel(int(self.config["blacklist_msg_channel_id"])) \
                            .send(f'{messageAuthor.mention} used a blacklisted word in {message.channel.mention}. They said: "{message.content}"')

                        if self.config["kick_on_blacklist"] == "True":
                            try:
                                await message.guild.kick(messageAuthor)
                                await self.bot.get_channel(int(self.config["blacklist_msg_channel_id"])) \
                                    .send(f'**{messageAuthor.mention}** is now kicked')
                                print(f'Kicked userid {messageAuthor.id} for writing blacklisted word in {message.channel.mention}. They said: "{message.content}"')
                            except MissingPermissions:
                                print("BOT is lacking permission to kick members")
