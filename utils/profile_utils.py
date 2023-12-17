import json, discord

with open("profile.json", "r") as f:
    profile_json = json.load(f)


def dump_profile_json(profile_json):
    # your code here
    with open("profile.json", "w") as f:
        json.dump(profile_json, f, indent=1)


def create_profile_embed(user: discord.Member) -> (discord.Embed, str):
    user_profile = profile_json["profiles"][str(user.id)]
    profile_embed = discord.Embed(
        title=user.global_name,
        description=f"User: {user.mention}",
        color=discord.Color.pink()
    ).set_thumbnail(url=user.display_avatar.url)
    with open("gatekeeper.json", "r") as f:
        gate = json.load(f)
    
    with open("verification.json", 'r') as f:
        verification = json.load(f)

    for age in gate["age"]:
        if user.guild.get_role(age["role"]) in user.roles:
            user_age = age["label"]
            break
    if user.guild.get_role(verification['male_role']) in user.roles:
        user_gender = "Male"
    if user.guild.get_role(verification['female_role']) in user.roles:
        user_gender = "Female"
    if user.guild.get_role(verification['trans_m_role']) in user.roles:
        user_gender = "Trans M"
    if user.guild.get_role(verification['trans_f_role']) in user.roles:
        user_gender = "Trans F"
    user_orientation = user_dm_status = "None"
    for orientation in profile_json["orientation_roles"]:
        if user.guild.get_role(orientation["role"]) in user.roles:
            user_orientation = orientation["label"].title()
            break
    for status in profile_json["dm_status_roles"]:
        if user.guild.get_role(status["role"]) in user.roles:
            user_dm_status = status["label"]
            break
    
    age_verified = user.guild.get_role(verification['18_verified_role'])
    female_verified = user.guild.get_role(verification['female_gender_verified_role'])
    male_verified = user.guild.get_role(verification['male_gender_verified_role'])
    m_trans_verified = user.guild.get_role(verification['f_to_m_verified_role'])
    f_trans_verified = user.guild.get_role(verification['m_to_f_verified_role'])
    a_verified, g_verified = (False, False)

    if age_verified in user.roles:
        a_verified = True
    
    if female_verified in user.roles or male_verified in user.roles or m_trans_verified in user.roles or f_trans_verified in user.roles:
        g_verified = True
    
    if a_verified and g_verified:
        user_verification = "Selfie and Age Verified"
    elif g_verified:
        user_verification = "Selfie Verified"
    else:
        user_verification = "Unverified"
    

    profile_embed.add_field(
        name="Name", value=user_profile["name"], inline=True
    ).add_field(name="Age", value=user_age, inline=True).add_field(
        name="Gender", value=user_gender, inline=True
    ).add_field(
        name="Orientation", value=user_orientation, inline=False
    ).add_field(
        name="Location", value=user_profile['location'], inline=True,
    ).add_field(
        name="Dating Status", value = user_profile['status'], inline=True,
    ).add_field(
        name = "Height", value = user_profile['height'], inline=True
    ).add_field(
        name='DM Status', value=user_dm_status, inline=True
    ).add_field(
        name='Verification Status', value=user_verification, inline=True
    ).add_field(
        name='Looking For', value=user_profile['seeking'], inline=False
    ).add_field(
        name='Hobbies', value=user_profile['hobbies'], inline=False
    ).add_field(
        name='About Me', value=user_profile['bio'], inline=False
    )
    if "selfie" in profile_json['profiles'][str(user.id)]:
        profile_embed.set_image(url='attachment://img.png')
        

    return profile_embed, str(user_gender)

def get_selfie(user: discord.Member):
    return discord.File(profile_json['profiles'][str(user.id)]['selfie'], filename='img.png')
