import sys
import traceback
from typing import Any, Callable, Coroutine, Dict, Optional

import discord
from discord import Interaction, User, VoiceChannel
from discord.ext.commands import command, Context

from helpers.config_loader import config, admin
from embeds.warningEmbeds import UserWarningEmbed

from .activities import Activity

async def _launch_response_kwargs(user: User, activity: Activity, voice_channel: VoiceChannel) -> Dict[str, Any]:
    try:
        invite = await activity.create_link(voice_channel)
    except discord.errors.Forbidden:
        warning = UserWarningEmbed(user=user, offense="Warning: Bot is missing permissions.", 
                                        description=f"This bot requires permission to create invites.",
                                        channel=user.get_channel(int(config["MemberWatch"]["bot_info_channel_id"])))
        warning.print_warning_to_console()
    except discord.errors.HTTPException:
        warning = UserWarningEmbed(user=user, offense="Warning: Failed to create an invite for Voice Activity.", 
                                        description=f"Please try a different activity.",
                                        channel=user.get_channel(int(config["MemberWatch"]["bot_info_channel_id"])))
        warning.print_warning_to_console()
    # send link
    return {"content": f"Click the blue link to start the activity!\n{invite.url}"}


async def start_activity(
    activity_key: Optional[str],
    *,
    ctx: Optional[Context] = None,
    interaction: Optional[Interaction] = None,
    voice_channel = Optional[VoiceChannel]
):
    """
    Sends a link to launch and join the activity

    Args:
        activity_key: key for the activity (eg. `youtube`, `chess`)
            If not specified, or an invalid key is provided, the user
            will be prompted to select an activity with buttons.
        ctx: Command context if applicable
        interaction: Interaction if applicable
    """
    message_kwargs = {"content": ""}
    # method to use for sending the link
    sender = ctx.send if ctx else interaction.send
    # user for creating the activity
    user = ctx.author if ctx else interaction.user
    # get the activity by the user-specified key
    activity = Activity.get_activity(activity_key)
    if activity is None:
        warning = UserWarningEmbed(user=user, offense="Error: Activity is not set", 
                                        description=f"Please try a different activity or check source code!",
                                        channel=user.get_channel(int(config["MemberWatch"]["bot_info_channel_id"])))
        warning.print_warning_to_console()
        
    # send response for launching activity
    message_kwargs |= await _launch_response_kwargs(user, activity, voice_channel)
    await sender(**message_kwargs)
