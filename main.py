import discord
from config import bot_token
from discord import Client


intents = discord.Intents.all()
client = Client(intents=intents)
msg_id = None
whitelist = 'Test'

embed = discord.Embed(
        title='Добро пожаловать в Wheel AIO',
        description='Что бы получить доступ к серверу и всем его возможностям поставьте реакцию под данным сообщением',
        color=0x488298
    )


@client.event
async def on_ready():
    print('Logged in')


@client.event
async def on_message(msg):
    if msg.content == 'Roles':
        guild_id = msg.guild.id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        user = discord.utils.find(lambda u: u.id == msg.author.id, guild.members)
        for role in user.roles:
            if str(role) == whitelist:
                global msg_id
                channel = client.get_channel(msg.channel.id)
                wh = await channel.send(embed=embed)
                await wh.add_reaction('✅')
                msg_id = wh.id
                await msg.delete()


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

    if message_id == msg_id:
        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='Check')

            if role is not None:
                user = discord.utils.find(lambda u: u.id == payload.user_id, guild.members)
                if user is not None:
                    await user.add_roles(role)
                else:
                    print('User is empty')


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

    if message_id == msg_id:
        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='Check')

            if role is not None:
                user = discord.utils.find(lambda u: u.id == payload.user_id, guild.members)
                if user is not None:
                    await user.remove_roles(role)
                else:
                    print('User is empty')


client.run(bot_token)
