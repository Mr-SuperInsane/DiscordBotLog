import discord
from discord.ext import commands
from discord.commands import Option

import sqlite3
import csv
import os
from datetime import datetime
from pytz import timezone

# Replace this code with your env.
TOKEN = '' 
bot = commands.Bot(command_prefix=".", case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help")

# this code is required
your_country = ''

# -------------------------------

# user join the server
@bot.event
async def on_member_join(member):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    type_value = 'user_join'
    user_id_value = member.id
    display_name_value = member.display_name
    time_value = datetime.now(timezone(your_country)).strftime('%Y-%m-%d %H:%M')
    cur.execute(
        "INSERT INTO log (type, user_id, display_name, time) VALUES (?, ?, ?, ?)",
        (type_value, user_id_value, display_name_value, time_value)
    )
    conn.commit()
    conn.close()

#  user remove the server
@bot.event
async def on_member_remove(member):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    type_value = 'user_remove'
    user_id_value = member.id
    display_name_value = member.display_name
    time_value = datetime.now(timezone(your_country)).strftime('%Y-%m-%d %H:%M')
    cur.execute(
        "INSERT INTO log (type, user_id, display_name, time) VALUES (?, ?, ?, ?)",
        (type_value, user_id_value, display_name_value, time_value)
    )
    conn.commit()
    conn.close()

# user send message
@bot.event
async def on_message(message):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    type_value = 'send_message'
    user_id_value = message.author.id
    display_name_value = message.author.display_name
    channel_value = message.channel.id
    message_value = message.content
    time_value = datetime.now(timezone(your_country)).strftime('%Y-%m-%d %H:%M')
    cur.execute(
        "INSERT INTO log (type, user_id, display_name, time, channel, message) VALUES (?, ?, ?, ?, ?, ?)",
        (type_value, user_id_value, display_name_value, time_value, channel_value, message_value)
    )
    conn.commit()
    conn.close()

# user delete message
@bot.event
async def on_message_delete(message):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    type_value = 'delete_message'
    user_id_value = message.author.id
    display_name_value = message.author.display_name
    channel_value = message.channel.id
    message_value = message.content
    time_value = datetime.now(timezone(your_country)).strftime('%Y-%m-%d %H:%M')
    cur.execute(
        "INSERT INTO log (type, user_id, display_name, time, channel, message) VALUES (?, ?, ?, ?, ?, ?)",
        (type_value, user_id_value, display_name_value, time_value, channel_value, message_value)
    )
    conn.commit()
    conn.close()

# user edit message
@bot.event
async def on_message_edit(before, after):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    type_value = 'edit_message'
    user_id_value = before.author.id
    display_name_value = before.author.display_name
    channel_value = before.channel.id
    message_value = before.content
    new_message_value = after.content
    time_value = datetime.now(timezone(your_country)).strftime('%Y-%m-%d %H:%M')
    cur.execute(
        "INSERT INTO log (type, user_id, display_name, time, channel, message, new_message) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (type_value, user_id_value, display_name_value, time_value, channel_value, message_value, new_message_value)
    )
    conn.commit()
    conn.close()

# admin command
# this command export csv file of log data in dm.
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def export_log_file(ctx):
    await ctx.response.defer()
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM log")
    rows = cur.fetchall()
    with open('log_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "type", "user_id", "display_name", "time", "channel", "message", "new_message"
        ])
        writer.writerows(rows)
        f.close()
    conn.close()
    with open('log_data.csv', mode='rb') as f:
        await ctx.user.send(file=discord.File(f))
        f.close()
    await ctx.delete()

# admin command
# this command change log data to csv file in the server. (this command doesn't send anything.)
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def converter_log_to_csv(ctx):
    await ctx.response.defer()
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM log")
    rows = cur.fetchall()
    with open('log_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "type", "user_id", "display_name", "time", "channel", "message", "new_message"
        ])
        writer.writerows(rows)
        f.close()
    conn.close()
    await ctx.delete()

# admin command
# this command get data from time. (Enter the beginning of time(arg1) and end fo time(arg2) you want to search for.)
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def select_data_from_time(ctx, start_time: Option(str, description="Beginning of time range"), end_time: Option(str, description="End of time range")):
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM log WHERE time BETWEEN '{start_time}' AND '{end_time}'"
    )
    rows = cur.fetchall()
    for row in list(rows):
        try:
            await ctx.send(str(row))
        except:
            pass
    conn.close()

# admin command
# this command get data from column name and value. (You can get data matching the column name(arg1) and value(arg2) you entered.)
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def select_data_from_column_and_data(ctx, column: Option(str, description="column name"), data: Option(str, description="value")):
    await ctx.response.defer()
    dbname = 'log.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    query = f"SELECT * FROM log WHERE {column} = '{data}'"
    cur.execute(query)
    rows = cur.fetchall()
    for row in list(rows):
        try:
            await ctx.send(str(row))
        except:
            pass
    conn.close()
    await ctx.delete()


while __name__ == '__main__':
    try:
        dbname = 'log.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY,type TEXT NOT NULL,user_id TEXT NOT NULL,display_name TEXT NOT NULL,time TEXT,channel TEXT,message TEXT,new_message TEXT)"
        )
        conn.commit()
        conn.close()
        bot.run(TOKEN)
    except discord.errors.HTTPException as e:
        print(e)
        os.system('kill 1')