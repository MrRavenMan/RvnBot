from discord.errors import Forbidden
from discord.ext.commands import Cog, slash_command, has_any_role
from discord.channel import DMChannel
from discord import File, Option, Member

import re
import json
import datetime
import pickle
import time
import matplotlib.pyplot as plt


from helpers.config_loader import config, admin
from embeds.warningEmbeds import UserWarningEmbed, WarningEmbed
from embeds.infoEmbeds import JoinEmbed, LeaveEmbed, BotStatusEmbed
from embeds.dataEmbeds import ReportEmbed, UserReportEmbed
from views.punishButtonsView import PunishButtonsView



class MemberWatch(Cog):
    def __init__(self, client):
        self.bot = client

        self.blacklist_words = []
        self.blacklist_paragraphs = []
        self.user_warnings = {}

        try:
            self.load_data()
        except FileNotFoundError:
            self.data = {"joins": [], "leaves": [], "warnings": [], "warned_users": {}, "kicks": [], "kicked_users": {}, "bans": [], "timeouts": [], "timeouted_users": {},
                        "blacklist_removals": [], "blacklisted_words": {}, "blacklist_users": {}, "warning_dms": [], "data_start": time.time()}

        self.recent_kick_or_banned_users = []


    @Cog.listener()
    async def on_ready(self):
        print("Member Watch Module: ONLINE")
        await self.load_blacklist(startup=True)
        if datetime.datetime.utcnow().strftime("%d") == "1":
            await self.report_data()

    @Cog.listener()
    async def on_member_join(self, member):
        self.data["joins"].append(time.time())
        sent_msg = False
        for user in self.recent_kick_or_banned_users:
            if user == member.id:
                await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"{member.mention} has joined the server. This user was recently kicked from the server!")
                print(f"member {member.name}#{member.discriminator} joined. This user was recently kicked from the server")
                sent_msg = True
        if sent_msg is False:
            await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"{member.mention} has joined the server.")
            print(f"member {member.name}#{member.discriminator} joined")

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
        self.data["leaves"].append(time.time())
        # embed = LeaveEmbed(member)
        # await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(embed=embed)

        sent_msg = False
        for user in self.recent_kick_or_banned_users:
            if user == member.id:
                await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"**{member.name}#{member.discriminator}** has been kicked out of the server.")
                print(f"member {member.name}#{member.discriminator} has been kicked out of the server")
                sent_msg = True
        if sent_msg is False:
            await self.bot.get_channel(int(config["MemberWatch"]["join_msg_channel_id"])).send(content=f"**{member.name}#{member.discriminator}** has left the server.")
            print(f"member {member.name}#{member.discriminator} left")

    @Cog.listener() 
    async def on_message(self, message): # blacklist logic
        messageAuthor = message.author
    
        if messageAuthor != self.bot.user: # check if message is by bot itself or whitelisted role
            if (isinstance(message.channel, DMChannel) == False):
                bannedItem = self.contains_blacklisted(message.content.lower(), messageAuthor)
                if bannedItem is None: # Exit func if not banned item in msg
                    return

                await message.delete()
                self.data["blacklist_removals"].append(time.time())
                if bannedItem.word in self.data["blacklisted_words"]:
                    self.data["blacklisted_words"][bannedItem.word] += 1
                else:
                    self.data["blacklisted_words"][bannedItem.word] = 1

                if f"{messageAuthor.name}#{messageAuthor.discriminator}" in self.data["blacklist_users"]:
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words_cnt"] += 1
                    if bannedItem.word in self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words"]:
                        self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words"][bannedItem.word] += 1
                    else:
                        self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words"][bannedItem.word] = 0
                else:
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] = {}
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words_cnt"] = 1
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words"] = {}
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words"][bannedItem.word] = 1
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["last_moderator_warning"] = 0

                # For every 10 messages RvnBot deletes from a single user due to use of blacklisted words, send warning message to server moderators
                if self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["blacklisted_words_cnt"] >= self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["last_moderator_warning"] + 10:
                    mod_warning_embed = WarningEmbed()
                    mod_warning_embed.title = "**USER WARNING**"
                    mod_warning_embed.add_field(name="User:", value=f"{messageAuthor.mention}")
                    mod_warning_embed.add_field(name="Warning", value=f"Excessive use of blacklisted words", inline=False)
                    mod_warning_embed.add_field(name="Message", value=f"{self.bot.user.name} has deleted {self.data['blacklist_users'][f'{messageAuthor.name}#{messageAuthor.discriminator}']['blacklisted_words_cnt']} \
                                                                        messages sent by this user containing blacklisted words. \n Keep an eye on this one!", inline=False)
                    await self.bot.get_channel(int(config["MemberWatch"]["blacklist_msg_channel_id"])).send(embed=mod_warning_embed)
                    self.data["blacklist_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"]["last_moderator_warning"] = self.data['blacklist_users'][f'{messageAuthor.name}#{messageAuthor.discriminator}']['blacklisted_words_cnt']
                

                message.content = message.content.replace("@", "*@*") # Make sure bot doesn't tag everyone when sending admins blacklist msg
                warning_embed = UserWarningEmbed(user=messageAuthor, offense="Use of blacklisted item", description=f"They said: '{message.content}'",
                                        channel=message.channel)

                try:
                    if bannedItem.user_msg_path is not None: # Send msg to user
                        await messageAuthor.send((self.user_warnings[bannedItem.user_msg_path].format(user_mention=f"{messageAuthor.name}#{messageAuthor.discriminator}",
                                                                                    channel_mention=message.channel.name,
                                                                                    message=message.content,
                                                                                    server_mention=message.guild.name)))
                        self.data["warning_dms"].append(time.time())


                    if bannedItem.ban_on_use:
                        self.recent_kick_or_banned_users.append(messageAuthor.id)

                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has been banned. \
                        Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await message.guild.ban(messageAuthor, reason=reason)
                        warning_embed.add_reaction("User has been banned") 

                        self.data["bans"].append(time.time())
                        

                    if bannedItem.kick_on_use:
                        self.recent_kick_or_banned_users.append(messageAuthor.id)
                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has been kicked. \
                        Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await message.guild.kick(messageAuthor, reason=reason)
                        warning_embed.add_reaction("User has been kicked")

                        self.data["kicks"].append(time.time())
                        if f"{messageAuthor.name}#{messageAuthor.discriminator}" in self.data["kicked_users"]:
                            warning_embed.add_repeat_offender("kicked", self.data["kicked_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"])
                            self.data["kicked_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] += 1
                        else:
                            self.data["kicked_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] = 1

                    if bannedItem.timeout():
                        reason = f"{messageAuthor.name}#{messageAuthor.discriminator} has gotten timeout until {(datetime.datetime.utcnow() + bannedItem.timeout_period).strftime('%Y-%m-%d %H:%M:%S')}. \
                            Reason: Wrote blacklisted word in {message.channel.name}. {messageAuthor.name} said: {message.content}"
                        await messageAuthor.timeout_for(duration=bannedItem.timeout_period, reason=reason)
                        warning_embed.add_reaction(f"User has been given timeout until {(datetime.datetime.utcnow() + bannedItem.timeout_period).strftime('%Y-%m-%d %H:%M:%S')}")

                        self.data["timeouts"].append(time.time())
                        if f"{messageAuthor.name}#{messageAuthor.discriminator}" in self.data["timeouted_users"]:
                            self.data["timeouted_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] += 1
                            warning_embed.add_repeat_offender("given timeout", self.data["timeouted_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"])
                        else:
                            self.data["timeouted_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] = 1

                    if bannedItem.warn_on_use:
                        if bannedItem.user_msg_path is None: # Send standard warning if no custom warning is defined
                            await messageAuthor.send(f"{messageAuthor.name}#{messageAuthor.discriminator} this is a warning for using a banned word. \n Reason: You wrote blacklisted word in {message.channel.name}. You said: {message.content} \n Note that this sentence contains one or more banned words and therefore have been deleted")
                        warning_embed.add_reaction(f"User has been warned.")

                        self.data["warnings"].append(time.time())
                        if f"{messageAuthor.name}#{messageAuthor.discriminator}" in self.data["warned_users"]:
                            self.data["warned_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] += 1
                            warning_embed.add_repeat_offender("warned", self.data["warned_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"])
                        else:
                            self.data["warned_users"][f"{messageAuthor.name}#{messageAuthor.discriminator}"] = 1
                        self.recent_kick_or_banned_users.append(messageAuthor.id)


                    if bannedItem.allow_user_options and bannedItem.ban_on_use is False and bannedItem.kick_on_use is False:
                        self.recent_kick_or_banned_users.append(messageAuthor.id)
                        view = PunishButtonsView(bot=self.bot, offender=messageAuthor, message=message, blacklist_msg_channel_id=bannedItem.blacklist_msg_channel_id, warning_embed=warning_embed)
                        await self.bot.get_channel(bannedItem.blacklist_msg_channel_id).send(content=f"", embed=warning_embed, view=view)
                        self.bot.add_view(PunishButtonsView(bot=self.bot, offender=messageAuthor, message=message, blacklist_msg_channel_id=bannedItem.blacklist_msg_channel_id, warning_embed=warning_embed))
                    elif bannedItem.alow_user_options is False and (bannedItem.ban_on_use or bannedItem.kick_on_use or bannedItem.warn_on_use or bannedItem.timeout > 0):
                        await self.bot.get_channel(bannedItem.blacklist_msg_channel_id).send(embed=warning_embed)
                        warning_embed.print_warning_to_console()

                    self.save_data()
                    return

                except Forbidden:
                        print(f"BOT is lacking permissions to act against user {messageAuthor.name}#{messageAuthor.discriminator} \
                        They used blacklisted phrase: '{message.content}' in {message.channel.name}")

    @slash_command(name="blacklist", description=f'Reload blacklist')  # Command to reload blacklist
    @has_any_role(admin, config["MemberWatch"]["manage_blacklist"])
    async def blacklist(self, ctx,):
        await self.load_blacklist()
        await ctx.interaction.response.send_message(content=f"Blacklist reloaded", delete_after=3)

    @slash_command(name="report", description=f'Generate Statistics')  # Command to generate statistics
    @has_any_role(admin, config["MemberWatch"]["query_reports"])
    async def data_report(self, ctx,):
        await self.report_data()
        await ctx.interaction.response.send_message("Server report:", delete_after=0.1)

    @slash_command(name="report_short", description=f'Generate Quick Statistics')  # Command to generate statistics
    @has_any_role(admin, config["MemberWatch"]["query_reports"])
    async def data_report_short(self, ctx,):
        await self.report_data(short=True)
        await ctx.interaction.response.send_message("Server report:", delete_after=0.1)

    @slash_command(name="user_report", description=f'See report for user')  # Command to reset member data
    @has_any_role(admin, config["MemberWatch"]["query_reports"])
    async def user_report(self, ctx, user: Option(Member, description="Member to see report of", required=True)):
        user_report_embed = UserReportEmbed(self.data, f"{user.name}#{user.discriminator}")
        await ctx.interaction.response.send_message(embed=user_report_embed)

    @slash_command(name="data_export", description=f'Export member data to JSON file')  # Command to export member data to JSON file
    @has_any_role(admin, config["MemberWatch"]["manage_reports"])
    async def data_export(self, ctx,):
        # self.export_data()
        await ctx.interaction.response.send_message(content=f"Method currently not implemented", delete_after=3)

    @slash_command(name="data_reset", description=f'Reset Member data')  # Command to reset member data
    @has_any_role(admin, config["MemberWatch"]["manage_reports"])
    async def data_reset(self, ctx,):
        self.data = {"joins": [], "leaves": [], "warnings": [], "warned_users": {}, "kicks": [], "kicked_users": {}, "bans": [], "timeouts": [], "timeouted_users": {},
                        "blacklist_removals": [], "blacklisted_words": {}, "blacklist_users": {}, "warning_dms": [], "data_start": time.time()}
        self.save_data()
        await ctx.interaction.response.send_message(content=f"Data reset", delete_after=3)

    def export_data(self):
        with open(f"Member DATA {datetime.datetime.utcnow()}.json", "w") as write_file:
            json.dump(self.data, write_file, indent=4)

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
                                        blacklist_msg_channel_id=sub_blacklist["blacklist_msg_channel_id"]
                                        )
                blacklisted_item.warn_on_use = blacklisted_item.warn_on_use[0] # This is due to line: warn_on_use=bool(sub_blacklist["warn_on_use"]) somehow returning a tuple instead of bool
                # No clue why this bug occurs
                blacklisted_item.user_msg_path = blacklisted_item.user_msg_path[0] # Same issue as above :/

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

    def save_data(self):
        with open('memberWatchModule_DATA.pickle', 'wb') as f:
            pickle.dump(self.data, f)    
    
    def load_data(self):
        with open('memberWatchModule_DATA.pickle', 'rb') as f:
            self.data = pickle.load(f)

    {"joins": [], "leaves": [], "warnings": [], "warned_users": {}, "kicks": [], "kicked_users": {}, "bans": [], "timeouts": [], "timeouted_users": {},
                        "blacklist_removals": [], "blacklisted_words": {}, "blacklist_users": {}, "warning_dms": [], "data_start": time.time()}

    async def report_data(self, short=False):
        report_embed = ReportEmbed(data=self.data)
        await self.bot.get_channel(int(config["MemberWatch"]["blacklist_msg_channel_id"])).send(content=f"", embed=report_embed)
        if not short:
            await self.generate_data_plots(self.data["joins"], "Members joined", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["leaves"], "Members left", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["blacklist_removals"], "Blacklist Removals", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["warnings"], "Warnings", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["timeouts"], "Timeouts", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["kicks"], "Kicks", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
            await self.generate_data_plots(self.data["bans"], "Bans", self.bot.get_channel(int(config["MemberWatch"]["report_msg_channel_id"])))
        
    async def generate_data_plots(self, data, action_name, channel):
        plt.style.use('seaborn')

        action_dates = []
        action_dates_clean = []
        action_count = []
        for action in data:
            date = datetime.datetime.fromtimestamp(action).date()
            action_dates.append(date)

        action_count_dict = {i:action_dates.count(i) for i in action_dates}
        for key, date in action_count_dict.items():
            action_dates_clean.append(key)
            action_count.append(date)
        
        plt.plot_date(action_dates_clean, action_count, linestyle='solid')
        plt.xlabel('Date') 
        plt.ylabel(action_name) 
        plt.title(action_name)
        plt.tight_layout()
        filepath = f"DataPlots/{action_name}.png"
        plt.savefig(filepath)
        await channel.send(file=File(filepath))
        

class BlacklistedItem():
    def __init__(self, word: str = "", timeout_period: datetime.timedelta = None, kick_on_use: bool = False,
     ban_on_use: bool = False, warn_on_use: bool = True, allow_user_options: bool = False, full_word: bool = True, user_msg_path = None, whitelisted_role_ids = [], blacklist_msg_channel_id = int(config["MemberWatch"]["blacklist_msg_channel_id"])):
        self.word = str(word.lower().replace("@", "add_"))
        self.timeout_period = timeout_period
        self.kick_on_use = kick_on_use
        self.ban_on_use = ban_on_use
        self.warn_on_use = warn_on_use,
        self.allow_user_options = allow_user_options,
        self.full_word = full_word
        self.whitelisted_role_ids = whitelisted_role_ids
        self.user_msg_path = user_msg_path,
        self.blacklist_msg_channel_id = blacklist_msg_channel_id

    def timeout(self) -> bool:
        if self.timeout_period is None:
            return False
        return True

