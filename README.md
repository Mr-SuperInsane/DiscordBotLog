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

# Manage data

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
- user_id
- display_name
- time

## Messages sent

- id(primary key)
- type('send_message')
- user_id
- display_name
- time
- message

## Editing messages

- id(primary key)
- type('edit_message')
- user_id
- display_name
- time
- message
- new_message

## Deleting messages

- id(primary key)
- type('delete_message')
- user_id
- display_name
- time
- message

# Admin command

Administrators can use several commands to manage the DB.

- export_log_file
- converter_log_to_csv
- select_data_from_time
- select_data_from_column_and_data

How to use these commands.

## export_log_file

This command can be used to get csv file of all log data.

## converter_log_to_csv

This command can be used to change all log data to csv file.  
This command don't send anything.

## select_data_from_time

This command can be used to get all data for the time you specify.
Enter the beginning of time and end of time(arg2) you want to search for.  
arg1 : Beginning of time range  
arg2 : End of time range.  

However, it must be entered in the following this format.
```
year-month-day hour:minute
```
example
```
2023-1-1 10:30
```
> And if the number of characters in each message is too large, an error may occur.

## select_data_from_column_and_data

This command can be used to get all data from column name and value.  
You can get data matching the column name(arg1) and value(arg2) you entered.

> And if the number of characters in each message is too large, an error may occur.

