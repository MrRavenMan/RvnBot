import discord
  
async def set_status(client, status, status_msg, status_streaming_url):
    try: # Add custom status
        if (int(status) == 1):
            print(f"Using status {status}: Playing {status_msg}")
            await client.change_presence(activity=discord.Game(name=status_msg))
        elif (int(status) == 2):
            print(f"Using status 2: Streaming {status_msg}. Link: {status_streaming_url}")
            await client.change_presence(activity=discord.Streaming(name=status_msg, url=status_streaming_url))
        elif (int(status) == 3):
            print(f"Using status {status}: Playing {status_msg}")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_msg))
        elif (int(status) == 4):
            print(f"Using status {status}: Playing {status_msg}")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status_msg))
        elif (int(status) == 5):
            print(f"Using status {status}: Playing {status_msg}")
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_msg))
    except ValueError:
        print("Error loading status. \n Make sure Status in config is a number. Set status to 0 to turn status off")
    except:
        print("ERROR (Non valueError) loading status")