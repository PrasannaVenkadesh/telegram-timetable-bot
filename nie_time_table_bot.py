#!/usr/bin/env python
__author__ = "Prasann Venkadesh <prashere@tuta.io>"
__license__ = "GPLV3"

"""
This program / script <whatever you call it> is a Free Software.
Which means, you are free to download, run, modify, distribute or
redistribute without seeking my permission. To know more about the
license please read through the `license.txt` file with this repo.

This is a telegram bot script that I wrote which when called with
specific commands will reply with the respective academic class
schedule for the day.

This script can be improved a lot. I have intentionally structured
it in a bad way (for example, could have created generic functions) 
hoping any of my class mates would pick it up & make it better.
"""

import os
import telegram
from datetime import datetime

# value / data specific for this progam

# Bot token acquired from Telegram @botfather
# retrieving from env variable
bot_settings = {"token": os.environ.get('TIMETABLE_BOT')}

# the timetable specific to our class
time_table = {0: "NCD(9:30-10:30), MNE(10:30-11:30), UE(11:30-1), IWT-LAB(2:30-4:30)",
              1: "NCD(9:30-11:30), DBT(11:30-1:30), CNP(2:30-4:30)", 
              2: "CNP(10:30-11:30), IWT(11:30-12:30), CNP-LAB(2:30-4:30)", 
              3: "DBT(9:30-10:30), UE(10:30-12:00), IWT(2:30-4:30)", 
              4: "MNE(10:30-12:30)"}

if __name__ == "__main__":

    # a file to track the last received message
    data_file_path = os.environ.get('HOME') + '/.putimetable_bot'
    
    # initiating the bot instance with it's settings
    bot = telegram.Bot(token=bot_settings.get('token'))
    
    # api call to telegram that gets the messages to this script
    messages_to_bot = bot.getUpdates()
    
    # actual logic that does reads and reply to the messages
    # self explanatory with corresponding variable names
    for a_message in messages_to_bot:
        message_text = a_message.message.text
        current_message_id = a_message.message.message_id
        chat_id = a_message.message.chat_id
        
        with open(data_file_path, 'r+') as data_file:
            # get the previous message count from the file
            previous_message_id = long(data_file.read().strip())
            
            if current_message_id > previous_message_id:
                data_file.seek(0)
                data_file.write(str(current_message_id))
                data_file.truncate()
                
                # get the current weekday from system
                today = datetime.today().weekday()
                day = -1
    

		# supported commands            
                if message_text == "/today":
                    day = today
                elif message_text == "/tomorrow" and today == 6:
                    day = 0
		elif message_text == "/tomorrow" and today != 6:
		    day = today + 1
                else:
                    message = "Well I am a kid. You people have to teach me. Demand source code from @prashere and train me. For now I can only reply to /today & /tomorrow commands."
                    bot.sendMessage(chat_id=chat_id, reply_to_message_id=current_message_id, text=message)
                    break;

		# the default message for weekdays.
                message = "It's <DAYHERE> and this is our schedule for the day.\n"
                    
                if day == 0:
                    message = message.replace('<DAYHERE>', "Monday")
                elif day == 1:
                    message = message.replace('<DAYHERE>', "Tuesday")
                elif day == 2:
                    message = message.replace('<DAYHERE>', "Wednesday")
                elif day == 3:
                    message = message.replace('<DAYHERE>', "Thursday")
                elif day == 4:
                    message = message.replace('<DAYHERE>', "Friday")
                elif day == 5 or day == 6:
                    message = "It's Weekend. Enjoy the day!"
                elif day == -1 or day > 6:
                    break;
                
		if message.find('Weekend') is not -1:
		    pass
		else:
                    message = message + time_table.get(day)
                
		# the bot sends the reply to the user / group that requested
		bot.sendMessage(chat_id=chat_id, reply_to_message_id=current_message_id, text=message)
