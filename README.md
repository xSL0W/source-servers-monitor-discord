# source-servers-monitor-discord
source-servers-monitor-discord

# What does this do?
This is a discord bot that counts number of connected players/map played on your source servers. It also can count a total of players.

# How does this look like on discord

![This is an image](https://i.imgur.com/qbFtS11.png)

# Ways of working

1) For every individual source server you have
2) Counting a total of players across all servers you have


# How to configure the bot

## Configuration of settings.json

Grab your bot token from discord developers (https://discord.com/developers/applications) and put it here

## Configuration of servers.cfg
Here you can put your server's DNS/IP or all your server's if you want the bot to count a total of players
No comments allowed, nothing else than IPs/DNS separated by a new line.

## Installation of dependencies

```
git clone https://github.com/xSL0W/source-servers-monitor-discord
cd source-servers-monitor-discord
apt install python3 python3-pip
pip3 install a2s-valve discord.py
python3 main.py
```

