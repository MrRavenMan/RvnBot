from discord import utils, Embed, Colour, File, Forbidden


async def assign(user, role):  # Function for assigning a member a role
        member = user
        if role not in member.roles:
            await member.add_roles(role)
            print(f"{member.name} has been assigned the role of {role.name}")

async def unassign(user, role):  # Function for unassigning a member a role
    member = user
    if role in member.roles:
        await member.remove_roles(role)
        print(f"{member.name} has been unassigned the role of {role.name}")
    
async def invert(user, role):  # Function for inverting (assigning/unassigning a mebmer a role)
    member = user
    if role not in member.roles:
        await member.add_roles(role)
        print(f"{member.name} has been assigned the role of {role.name}")
    elif role in member.roles:
        await member.remove_roles(role)
        print(f"{member.name} has been unassigned the role of {role.name}")
