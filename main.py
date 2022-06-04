#   MIT License
#   
#   Copyright (c) 2022 - Stan '(xSLOW)' Valentin-Alexandru 
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.



#    $$$$$$\                                                           $$$$$$\                                                                    $$\      $$\                     $$\   $$\                         
#   $$  __$$\                                                         $$  __$$\                                                                   $$$\    $$$ |                    \__|  $$ |                        
#   $$ /  \__| $$$$$$\  $$\   $$\  $$$$$$\   $$$$$$$\  $$$$$$\        $$ /  \__| $$$$$$\   $$$$$$\ $$\    $$\  $$$$$$\   $$$$$$\   $$$$$$$\       $$$$\  $$$$ | $$$$$$\  $$$$$$$\  $$\ $$$$$$\    $$$$$$\   $$$$$$\  
#   \$$$$$$\  $$  __$$\ $$ |  $$ |$$  __$$\ $$  _____|$$  __$$\       \$$$$$$\  $$  __$$\ $$  __$$\\$$\  $$  |$$  __$$\ $$  __$$\ $$  _____|      $$\$$\$$ $$ |$$  __$$\ $$  __$$\ $$ |\_$$  _|  $$  __$$\ $$  __$$\ 
#    \____$$\ $$ /  $$ |$$ |  $$ |$$ |  \__|$$ /      $$$$$$$$ |       \____$$\ $$$$$$$$ |$$ |  \__|\$$\$$  / $$$$$$$$ |$$ |  \__|\$$$$$$\        $$ \$$$  $$ |$$ /  $$ |$$ |  $$ |$$ |  $$ |    $$ /  $$ |$$ |  \__|
#   $$\   $$ |$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$   ____|      $$\   $$ |$$   ____|$$ |       \$$$  /  $$   ____|$$ |       \____$$\       $$ |\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$\ $$ |  $$ |$$ |      
#   \$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |      \$$$$$$$\ \$$$$$$$\       \$$$$$$  |\$$$$$$$\ $$ |        \$  /   \$$$$$$$\ $$ |      $$$$$$$  |      $$ | \_/ $$ |\$$$$$$  |$$ |  $$ |$$ |  \$$$$  |\$$$$$$  |$$ |      
#    \______/  \______/  \______/ \__|       \_______| \_______|       \______/  \_______|\__|         \_/     \_______|\__|      \_______/       \__|     \__| \______/ \__|  \__|\__|   \____/  \______/ \__|      
#                                                                                                                                                                                                                    
#                                                                                                                                                                                                                     
#   https://github.com/xSL0W?

# libraries
import discord
from discord.ext import tasks
from discord.errors import InvalidArgument

import a2s
import socket
import asyncio
import os
import json

# Main Code - Get settings
with open('settings.json') as json_file:
    data = json.load(json_file)
    for p in data['settings']:
        global REFRESH_TIME, TOKEN
        REFRESH_TIME = p['refresh-time']
        TOKEN = p['bot-token']


# dont change
VERSION = "0.1b"

# Global Variables
bot = discord.Client()


# On bot ready event. Called when the bot is loaded.
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('Im online :)')
    loop_renew_status.start()

# This will refresh the bot's status every REFRESH_TIME seconds
@tasks.loop(seconds=REFRESH_TIME)
async def loop_renew_status():
    await SetDiscordStatus(GenerateStatus())

# Set a status on discord
async def SetDiscordStatus(status = ""):
    activity = discord.Game(name=status, type=3)
    try:
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    except InvalidArgument:
        print("Exception: Invalid argument")
        pass
        
# Generate status by query-ing servers
def GenerateStatus():
    # initialize variables
    playercount = 0
    maxslots = 0
    count = 0
    map = ''

    # read file
    with open("servers.cfg", "r") as f:
        for line in f:
            line = line.rstrip() # remove whitespaces
            list = line.split(":", 2) # split text in 2 elements
            print("IP/DNS: " + list[0] + " PORT: " + list[1])
            
            # query servers
            address = (list[0], int(list[1]))
            try:
                csquery = a2s.info(address)

            except (socket.gaierror, a2s.BrokenMessageError, a2s.BufferExhaustedError, asyncio.exceptions.TimeoutError, socket.timeout, ConnectionRefusedError, OSError)  as e:
                print("### (WARNING) Exception occured while trying to query " + line + " - Please check for problems")
                continue   

            # increase playercount/maxslots
            playercount += csquery.player_count
            maxslots += csquery.max_players

            # get map name
            map = csquery.map_name

            # increase server count
            count = count + 1

        f.close() # close the file after using


    if count == 0: # Case if all servers are offline
        status = "Server(s) Offline"
    elif count == 1:
        status = str(playercount) + "/" + str(maxslots) + " on " + map
    elif count > 1: # Case if there are multiple servers
        status = str(playercount) + "/" + str(maxslots) + " on " + str(count) + " servers"

    print(status)
    return (status)


bot.run(TOKEN)