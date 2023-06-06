# DiscordBotLog

This code uses sqlite3 to manage all the discord bot logs.  

This code is designed to be integrated into a Discord Bot.

# Install Pycord

Python 3.8 or higher is required
```
# Linux/macOS
python3 -m pip install git+https://github.com/Pycord-Development/pycord

# Windows
py -3 -m pip install git+https://github.com/Pycord-Development/pycord
```

# How to use

You need to rewrite line 17 based on timezone of pytz.  
This is your time in the country in which you live.  
```
your_country = 'Asia/Tokyo'
```
  
If you don't know the timezone of pytz , please run this code in a separate file. You can find the region where you live.
```
import pytz
print(pytz.all_timezones)
```

# Specification

The contents stored in the log are as follows.  

- User participation
- User leaving
- Messages sent
- Editing messages
- Deleting messages

The following information is also stored.

## User participation

- id(primary key)
- type('user_join')
- user_id
- display_name
- time

## User leaving

- id(primary key)
- type('user_remove')
- 





