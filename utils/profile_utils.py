import json, discord
with open("profile.json", "r") as f:
    profile_json = json.load(f)

def dump_profile_json(profile_json):
    # your code here
    with open('profile.json', 'w') as f:
        json.dump(profile_json, f)

def create_profile_embed(user: discord.Member) -> discord.Embed:
    profile_embed = discord.Embed(
            title=user.global_name,
            description=f"User: {user.mention}",
            color=discord.Color.pink(),
        ).set_thumbnail(url=user.display_avatar.url)
    
    return profile_embed