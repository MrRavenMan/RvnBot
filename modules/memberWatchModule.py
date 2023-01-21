from discord.errors import Forbidden
from discord.ext.commands import Cog, slash_command, has_any_role
from discord.channel import DMChannel

import re
import json
import datetime

from helpers.config_loader import config, admin
from embeds.warningEmbeds import UserWarningEmbed
from embeds.infoEmbeds import JoinEmbed, LeaveEmbed, BotStatusEmbed
from views.punishButtonsView import PunishButtonsView



class MemberWatch(Cog):
    def __init__(self, client):
        self.bot = client

        self.blacklist_words = []
        self.blacklist_paragraphs = []
        self.user_warnings = {}


    @Cog.listener()
    async def on_ready(self):
        print("Member Watch Module: ONLINE")
        await self.load_blacklist(startup=True)

    @Cog.listener()
    async def on_member_join(self, member):
        print(f"member {member.name}#{member.discriminator} joined")
        # embed = JoinEmbed(member)
        # await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(embed=embed)
        await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"{member.mention} has joined the server.")

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
        print(f"member {member.name}#{member.discriminator} left")
        # embed = LeaveEmbed(member)
        # await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(embed=embed)
        await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"**{member.name}#{member.discriminator}** has left the server.")

    @Cog.listener() 
    async def on_message(self, message): # blacklist logic
        messageAuthor = message.author
    
        if messageAuthor != self.bot.user: # check if message is by bot itself or whitelisted role
            if (isinstance(message.channel, DMChannel) == False):
                bannedItem = self.contains_blacklisted(message.content.lower(), messageAuthor)
                if bannedItem is None: # Exit func if not banned item in msg
                    return

                await message.delete()
                message.content = message.content.replace("@", "*@*") # Make sure bot doesn't tag everyone when sending admins blacklist msg
            
                warning_embed = UserWarningEmbed(user=messageAuthor, offense="Use of blacklisted item", description=f"They said: '{message.content}'",
                                        channel=message.channel)

                try:
                    if bannedItem.user_msg_path is not None: # Send msg to user
                        await messageAuthor.send((self.user_warnings[bannedItem.user_msg_path].format(user_mention=f"{messageAuthor.name}#{messageAuthor.discriminator}",
                                                                                    channel_mention=message.channel.name,
                                                                                    message=message.content,
                                                                                    server_mention=message.guild.name)))


                    if bannedItem.ban_on_use:
                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has been banned. \
                        Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await message.guild.ban(messageAuthor, reason=reason)
                        warning_embed.add_reaction("User has been banned") 
                    if bannedItem.kick_on_use:
                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has been kicked. \
                        Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await message.guild.kick(messageAuthor, reason=reason)
                        warning_embed.add_reaction("User has been kicked")
                    if bannedItem.timeout():
                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has gotten timeout until {(datetime.datetime.utcnow() + bannedItem.timeout_period).strftime('%Y-%m-%d %H:%M:%S')}. \
                            Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await messageAuthor.timeout_for(duration=bannedItem.timeout_period, reason=reason)
                        warning_embed.add_reaction(f"User has been given timeout until {(datetime.datetime.utcnow() + bannedItem.timeout_period).strftime('%Y-%m-%d %H:%M:%S')}")
                    if bannedItem.warn_on_use:
                        if bannedItem.user_msg_path is None: # Send standard warning if no custom warning is defined
                            await messageAuthor.send(f"{messageAuthor.name}#{messageAuthor.discriminator} this is a warning for using a banned word. \n Reason: You wrote blacklisted word in {message.channel.name}. You said: {message.content} \n Note that this sentence contains one or more banned words and therefore have been deleted")
                        warning_embed.add_reaction(f"User has been warned.")


                    if bannedItem.allow_user_options and bannedItem.ban_on_use is False and bannedItem.kick_on_use is False:
                        view = PunishButtonsView(bot=self.bot, offender=messageAuthor, message=message, blacklist_msg_channel_id=config["MemberWatch"]["blacklist_msg_channel_id"], warning_embed=warning_embed)
                        warning_embed_msg = await self.bot.get_channel(int(config["MemberWatch"]["blacklist_msg_channel_id"])).send(content=f"", embed=warning_embed, view=view)
                        self.bot.add_view(PunishButtonsView(bot=self.bot, offender=messageAuthor, message=message, blacklist_msg_channel_id=config["MemberWatch"]["blacklist_msg_channel_id"], warning_embed=warning_embed))
                    elif bannedItem.alow_user_options is None and (bannedItem.ban_on_use or bannedItem.kick_on_use or bannedItem.warn_on_use or bannedItem.timeout):
                        await self.bot.get_channel(int(config["MemberWatch"]["blacklist_msg_channel_id"])).send(embed=warning_embed)
                        warning_embed.print_warning_to_console()

                    return

                except Forbidden:
                        print(f"BOT is lacking permissions to act against user {messageAuthor.name}#{messageAuthor.discriminator} \
                        They used blacklisted phrase: '{message.content}' in {message.channel.name}")

    @slash_command(name="blacklist", description=f'Reload blacklist')  # Command to reload blacklist
    @has_any_role(admin, config["MemberWatch"]["manage_blacklist"])
    async def blacklist(self, ctx,):
        await self.load_blacklist()
        await ctx.interaction.response.send_message(content=f"Blacklist reloaded", delete_after=3)

    async def load_blacklist(self, startup=False): # Set startup to True if called by on_ready
        with open('config/memberWatchConfig/blacklist.json') as blacklist_file:
            blacklists = json.load(blacklist_file)
            # dirty_blacklist = blacklist_data["blacklisted_words"]
            # self.whitelisted_role_ids = blacklist_data["whitelisted_role_ids"]
        
        self.blacklist_words = []
        self.blacklist_paragraphs = []
        self.user_warnings = {}
        for sub_blacklist in blacklists:
            for item in sub_blacklist["blacklisted_items"]:
                timeout_period = None
                if int(sub_blacklist["timeout_minutes"]) != 0:
                    timeout_period = datetime.timedelta(minutes=int(sub_blacklist["timeout_minutes"]))

                # Set user_msg_path to none if no path is entered
                user_msg_path = sub_blacklist["user_msg_path"]
                if user_msg_path == "":
                    user_msg_path = None
                else: # load user warning into self.user_warnings dictionary
                    try:
                        with open (f"config/memberWatchConfig/userWarnings/{user_msg_path}", "r") as myfile:
                            data=myfile.readlines()
                        warning = ""
                        for i in data:
                            warning += i
                        self.user_warnings[user_msg_path] = warning
                    except:
                        print(f"WARNING Member Watch Module blacklist load error: An error occurred loading user warning with path '{user_msg_path}'")


                blacklisted_item = BlacklistedItem(word=item.lower(),
                                        timeout_period=timeout_period,
                                        kick_on_use=bool(sub_blacklist["kick_on_use"]),
                                        ban_on_use=bool(sub_blacklist["ban_on_use"]),
                                        warn_on_use=bool(sub_blacklist["warn_on_use"]),
                                        allow_user_options=bool(sub_blacklist["allow_user_options"]),
                                        full_word=bool(sub_blacklist["full_word"]),
                                        user_msg_path=user_msg_path,
                                        whitelisted_role_ids=sub_blacklist["whitelisted_role_ids"],
                                        )
                blacklisted_item.warn_on_use = blacklisted_item.warn_on_use[0] # This is due to line: warn_on_use=bool(sub_blacklist["warn_on_use"]) somehow returning a tuple instead of bool
                # No clue why this bug occurs

                if blacklisted_item.full_word is True:
                    self.blacklist_words.append((blacklisted_item))
                else:
                    self.blacklist_paragraphs.append(blacklisted_item)

        description = f"New blacklist loaded. It contains {len(self.blacklist_words) + len(self.blacklist_paragraphs)} blacklisted item"
        print(description)
        if not startup:
            embed = BotStatusEmbed(description=description)
            await self.bot.get_channel(int(config["General"]["bot_info_channel_id"])).send(embed=embed, delete_after=15)
            

    def msg_contains_word(self, msg, word):
        msg = msg.replace("@", "add_")
        return re.search(fr'\b({word})\b', msg) is not None # returns True if bad word is in message


    def contains_blacklisted(self, msg, author):
        for bannedWord in self.blacklist_words:
            if self.msg_contains_word(msg.lower(), bannedWord.word):
                if not any(role.id in bannedWord.whitelisted_role_ids for role in author.roles):
                    return bannedWord
        for bannedPhrase in self.blacklist_paragraphs:
            if bannedPhrase.word in msg:
                if not any(role.id in bannedWord.whitelisted_role_ids for role in author.roles):
                    return bannedPhrase
        return None        


class BlacklistedItem():
    def __init__(self, word: str = "", timeout_period: datetime.timedelta = None, kick_on_use: bool = False,
     ban_on_use: bool = False, warn_on_use: bool = True, allow_user_options: bool = False, full_word: bool = True, user_msg_path = None, whitelisted_role_ids = []):
        self.word = str(word.lower().replace("@", "add_"))
        self.timeout_period = timeout_period
        self.kick_on_use = kick_on_use
        self.ban_on_use = ban_on_use
        self.warn_on_use = warn_on_use,
        self.allow_user_options = allow_user_options,
        self.full_word = full_word
        self.whitelisted_role_ids = whitelisted_role_ids
        self.user_msg_path = user_msg_path

    def timeout(self) -> bool:
        if self.timeout_period is None:
            return False
        return True

