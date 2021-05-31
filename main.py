from datetime import date
import sys
import random
import discord
import sqlite3
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
from discord.ext import commands
import os

client = discord.Client()
slash = SlashCommand(client,sync_commands=True)
comms = commands.Bot(command_prefix="$")
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()


async def displayquotes(message):
    print('display quote requested')
    cursor.execute("SELECT rowid, quote FROM quotes")
    text = ""
    for item in cursor.fetchall():
        text = text + str(item[0])+":"+item[1]+"\n"
    return text


def getrandomquotes():
    cursor.execute("SELECT rowid,quote,date FROM quotes")
    print(cursor.fetchall())
    cursor.execute("SELECT rowid,quote,date FROM quotes")
    choice = random.choice(cursor.fetchall())
    print(choice)
    conn.commit()
    return choice[1]


def addquotes(text):
    today = date.today()
    today = today.strftime('%Y/%b/%d')
    cursor.execute("INSERT INTO quotes VALUES('1','{0}','{1}')".format(text, today))
    conn.commit()


def deleteRow(rowid):
    cursor.execute("DELETE FROM quotes WHERE rowid = {0}".format(rowid))
    conn.commit()


# slash commands overrides:


@slash.slash(description="Sends a random funny quote")
async def pepesays(ctx):
    await ctx.send("This works bro!")


@slash.slash(description="Lists all the available quotes with row id")
async def pepelist(ctx):
    await ctx.send(displayquotes())
    


@slash.slash(description="shows available commands and a brief description of the bot")
async def pepehelp(ctx):
    print('help command recieved')
    response = """
        Hello, Pepe bot was originally created as a learning process of discord bots.
        It is designed by Ashish Neupane (Unicodist)
        
        Available commands:
        */help* Displays this text
        */pepesays* Says something very wise
        *$pepe add ...* Adds a new wiseness into the database
        */pepelist* Lists the available quotes with their corresponding row number
        *$pepe delete <int>* Deletes a quotes corresponding to the given row number
    """
    await ctx.send(response)

# Slash commands overrides end
# Client events start


@client.event
async def on_ready():
    print("bot is online")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$pepe'):
        msg = message.content[6:]
        if msg.startswith("add"):
            msg = " ".join(msg.split(" ")[1:])
            addquotes(msg)
            await message.channel.send("The quote ***{0}*** has been added to out database".format(msg))
            return
        if msg.startswith("delete"):
            deleteRow(msg[-1])
            return


# Client events end
client.run("ODQ2OTY0MzAzMTIyOTIzNTgx.YK3K-Q.0ZJmrmFl0lRfPrOR3DKalNuNWfA")
