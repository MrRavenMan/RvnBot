from datetime import datetime
import time

from embeds.infoEmbeds import InfoEmbed

class ReportEmbed(InfoEmbed):
    def __init__(self, data):
        super().__init__()
        self.title = "Server Report"
        start = datetime.fromtimestamp(data["data_start"]).strftime('%Y-%m-%d %H:%M')
        
        joins = len(data["joins"])
        leaves = len(data["leaves"])
        self.add_field(name="Membership overview:", value=f"Since {start}: \n \
                                                              - {joins} users have joined the server \
                                                              \n - {leaves} users have left the server.", inline=False)

        blacklist_removals = len(data["blacklist_removals"])
        self.add_field(name="Blacklist overview:", value=f"Since {start}: \n   - {blacklist_removals} messages containing blacklisted words have been deleted", inline=False)

        warnings = len(data["warnings"])
        timeouts = len(data["timeouts"])        
        kicks = len(data["kicks"])
        bans = len(data["bans"])
        self.add_field(name="Punishment overview:", value=f"Since {start}: \
                                                            \n   - {warnings} warnings have been issued \
                                                            \n   - {timeouts} timeouts have been issued \
                                                            \n   - {kicks} kicks have been issued \
                                                            \n   - {bans} bans have been issued", inline=False)


        self.data = {"joins": [], "leaves": [], "warnings": [], "warned_users": {}, "kicks": [], "kicked_users": {}, "bans": [], "timeouts": [], "timeouted_users": {},
                        "blacklist_removals": [], "blacklisted_words": {}, "blacklist_users": {}, "warning_dms": [], "data_start": time.time()}
class UserReportEmbed(InfoEmbed):
    def __init__(self, data, username):
        super().__init__()
        self.title = "User Report"
        start = datetime.fromtimestamp(data["data_start"]).strftime('%Y-%m-%d %H:%M')

        warnings = 0
        timeouts = 0
        kicks = 0
        if username in data["warned_users"]:
            warnings = data["warned_users"][username]
        if username in data["timeouted_users"]:
            timeouts = data["timeouted_users"][username] 
        if username in data["kicked_users"]:
            kicks = data["kicked_users"][username]
        self.add_field(name="Punishment overview:", value=f"Since {start} user has received: \
                                                            \n   - {warnings} warnings \
                                                            \n   - {timeouts} timeouts\
                                                            \n   - {kicks} kicks", inline=False)

        blacklist_removals = data["blacklist_users"][username]["blacklisted_words_cnt"]
        msg = f"Since {start}: \n   - User has written a total of {blacklist_removals} messages with blacklisted words \n"
        for word, cnt in data["blacklist_users"][username]["blacklisted_words"].items():
            msg = msg + f'\n   - User has written "{word}" in {cnt} different messages \n'
        self.add_field(name="Blacklist overview:", value=msg, inline=False)
