from os import environ
from discord.ext import commands
import discord

role_id = int(environ['NEW_MEMBER_ROLE_ID'])
client = discord.Client()
newMembers = []


'''
    This function will calculate the seniority of a member, and return true if the member 
    has been in the server for less than 7 days
'''
def isNewMember(member, guild):
    mem_join = member.joined_at
    guild_create = guild.created_at
    join_days = (mem_join - guild_create).days
    return True if join_days < 7 else False


def checkIfThereAreMembersWithTheNewTag(guild, ctx):
    membersWithTheNewRole = []
    for member in guild.members:
        if discord.utils.find(lambda r: r.name == 'New Member', ctx.guild.roles) in member.roles:
            membersWithTheNewRole.append(member)
    return membersWithTheNewRole


def removeRoleFromOldMembers(newMembers, guild, role):
    if len(newMembers) != 0:
        notNewMembersAnymore = []
        for oldMember in newMembers:
            if isNewMember(oldMember, guild):
                notNewMembersAnymore.append(oldMember)
        for oldMember in notNewMembersAnymore:
            oldMember.remove_roles(role, reason=f"{oldMember.name} has been in the server for more than 7 days")


def updateSeniorityList(guild):
    for member in guild.members:
        if isNewMember(member, guild):
            newMembers.append(member)


def addRoleToNewMembers(guild, role):
    # New members get the role added to them, and they are added to a list of the previous
    for member in newMembers:
        member.add_roles(role, reason=f"{member.name} joined in the last 7 days")


@client.event
async def on_member_join(member):
    member.add_roles(role_id, reason=f"{member.name} just joined!")





# @commands.Cog.listener()
# async def on_voice_state_update(self, member, before, after):
#     try:
#         guild = self.bot.get_guild(member.guild.id)
#         role = guild.get_role(role_id)

#         # If this is the firs time we run the bot, it won't find any members from the previous day, so this part will be skipped
#         # If there is a list of the new members of the day before, it checks to see if they still have been on the server for less than 7 days
#         #   if they have been on the server for longer, the "new member" role is removed
#         removeRoleFromOldMembers(newMembers, guild, role)

#         # List of new members gets updated
#         updateSeniorityList(guild)

#         addRoleToNewMembers(guild, role)


    # finally:
    #     print()
