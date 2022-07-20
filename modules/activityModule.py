from random import choices
from discord.ext.commands import Cog, slash_command, has_any_role, command, Context
from discord import Option, VoiceChannel

from helpers.config_loader import config, admin
from helpers.voiceActivity.launch import start_activity


class VoiceActivities(Cog):
    def __init__(self, client):
        self.bot = client

    @Cog.listener()
    async def on_ready(self):
        print("Voice Activity Module: ONLINE")   

    if config.getboolean("VoiceActivities", "allow_youtube"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_youtube", description="Start watch together activity in a voice channel")    
        async def activity_youtube(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="youtube", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")
    
    if config.getboolean("VoiceActivities", "allow_poker"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_poker", description="Start watch together activity in a voice channel")    
        async def activity_poker(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="poker", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")
    
    if config.getboolean("VoiceActivities", "allow_chess"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_chess", description="Start watch together activity in a voice channel")    
        async def activity_chess(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="chess", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")

    if config.getboolean("VoiceActivities", "allow_checkers"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_checkers", description="Start watch together activity in a voice channel")    
        async def activity_checkers(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="checkers", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")

    if config.getboolean("VoiceActivities", "allow_betrayal"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_betrayal", description="Start watch together activity in a voice channel")    
        async def activity_betrayal(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="betrayal", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")

    if config.getboolean("VoiceActivities", "allow_fishington"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_fishington", description="Start watch together activity in a voice channel")    
        async def activity_fishington(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="fishington", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")

    if config.getboolean("VoiceActivities", "allow_letterleague"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_letterleague", description="Start watch together activity in a voice channel")    
        async def activity_letterleague(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="letterleague", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")

    if config.getboolean("VoiceActivities", "allow_wordsnacks"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_wordsnacks", description="Start watch together activity in a voice channel")    
        async def activity_wordsnacks(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="wordsnacks", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")
    
    if config.getboolean("VoiceActivities", "allow_sketchheads"):
        @has_any_role(admin, config["VoiceActivities"]["manage_voice_activities"])
        @slash_command(name="activity_sketchheads", description="Start watch together activity in a voice channel")    
        async def activity_sketchheads(self, ctx, voice_channel: Option(VoiceChannel,
                                                                    description="Voice channel to play in",
                                                                    required=True)):
            await start_activity(activity_key="sketchheads", voice_channel=voice_channel, interaction=ctx)
            await ctx.interaction.response.send_message("Generated activity: ")