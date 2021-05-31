from datetime import date
import random
import discord
import sqlite3
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext
from discord.ext import commands

client = discord.Client()
slash = SlashCommand(client,sync_commands=True)
comms = commands.Bot(command_prefix="$")
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()


async def displaycommands(message):
    await message.channel.send("""
                This is the showcase of pepe's commands
                Every command starts with $pepe:\n
                **say** Sends an epic random quote
                **add ...** is used to add new quotes in the database
                **help** shows command lists and description
                **list** Displays all the quotes in the database
                **delete *<int>* ** removes command with specified row id (can be seen with list command)
            *Created by*: Unicodist""")


async def displayquotes(message):
    cursor.execute("SELECT rowid, quote FROM quotes")
    text = ""
    for item in cursor.fetchall():
        text = text + str(item[0])+":"+item[1]+"\n"
    await message.channel.send(text)


def getrandomquotes():
    cursor.execute("SELECT rowid,quote,date FROM quotes")
    print(cursor.fetchall())
    cursor.execute("SELECT rowid,quote,date FROM quotes")
    choice = random.choice(cursor.fetchall())
    print(choice)
    conn.commit()
    return choice[1]


def getquotecount():
    cursor.execute("SELECT COUNT(*) from quotes")
    print(cursor.fetchone())
    conn.commit()


def addquotes(text):
    today = date.today()
    today = today.strftime('%Y/%b/%d')
    cursor.execute("""INSERT INTO quotes
                        VALUES('1','{0}','{1}')
                    """.format(text, today))
    conn.commit()



def deleteRow(rowid):
    cursor.execute("DELETE FROM quotes WHERE rowid = {0}".format(rowid))
    conn.commit()


# slash commands overrides:


@slash.slash(description="Sends a random funny quote")
async def pepesays(ctx):
    await ctx.send("This works bro!")


@slash.slash(description="shows available commands and a brief description of the bot")
async def pepehelp(ctx):
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

# Slash commands overrides end
# Client events start


@client.event
async def on_ready():
    print("The bot is online")


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
        if msg.startswith("say"):
            msg = getrandomquotes()
            await message.channel.send(message.author.mention+" "+msg)
            return
        if msg.startswith("help"):
            await displaycommands(message)
            return
        if msg.startswith("list"):
            await displayquotes(message)
            return
        if msg.startswith("delete"):
            deleteRow(msg[-1])
            return
        await displaycommands(message)


# Client events end
client.run("ODQ2OTY0MzAzMTIyOTIzNTgx.YK3K-Q.0ZJmrmFl0lRfPrOR3DKalNuNWfA")
