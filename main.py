import os
import discord
import requests


anime_commands = ['waifu','hug','kill','punch','kiss','slap','wink','pat','cuddle','boobs','lesbian','hentai']
anime_commands_nsfw = anime_commands[-3:]
print(anime_commands_nsfw)
client = discord.Client()
nsfw = False


async def anime(message):
  global nsfw
  global anime_commands
  msg = message.content[7:]
  if msg in anime_commands:
    if msg in anime_commands_nsfw:
      if nsfw:
        print("nsfw part")
        response = requests.get(f'https://anime-api.hisoka17.repl.co/img/nsfw/{msg}').json()
      else:
        await message.channel.send("NSFW is disabled bro :D")
        return
    else:
      response = requests.get(f'https://anime-api.hisoka17.repl.co/img/{msg}').json()
    picture = f"{response['url']}{'.jpg' if msg=='waifu' else ''}"
    await message.channel.send(picture)
  else:
    await message.channel.send(f""" Wrong command!
            Use one of these:
            {anime_commands}
    """)


@client.event
async def on_ready():
    print("READY")

@client.event
async def on_message(message):
    global nsfw

    if message.author == client.user:
        return

    if message.content.startswith('$anime '):
        await anime(message)

    if message.content.startswith('$joke'):
        response = requests.get(
            'https://official-joke-api.appspot.com/jokes/random').json()
        await message.channel.send(f"""{message.author.mention}
    **{response['setup']}**
    *{response['punchline']}*""")

    if message.content.startswith('$nsfw'):
        nsfw = not nsfw
        await message.channel.send(
            f"NSFW mode has been {'enabled' if nsfw else 'disabled'}.")


client.run("ODQ2OTY0MzAzMTIyOTIzNTgx.YK3K-Q.0ZJmrmFl0lRfPrOR3DKalNuNWfA")
