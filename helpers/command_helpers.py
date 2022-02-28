import time

async def cmd_acknowledge(ctx, reaction='\N{THUMBS UP SIGN}', response_time=0.5):
    await ctx.message.add_reaction(reaction)
    time.sleep(response_time)
    await ctx.message.delete()