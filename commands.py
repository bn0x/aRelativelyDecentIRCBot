import irc.bot
import irc.strings
import json
from irc.bot import ServerSpec
from irc.client import ip_numstr_to_quad
from irc.client import ip_quad_to_numstr

def cmd_ping(conn, event):
    conn.privmsg(event.target, 'pong')

def cmd_say(conn, event):
    conn.privmsg(event.target, ' '.join(event.arguments[0].split()[1:]))

def cmd_help(conn, event):
    conn.privmsg(event.target, "To get help please visit http://hitbox.tv/awfulbot or ask http://hitbox.tv/awful aka http://twitter.com/ejectment")

def cmd_about(conn, event):
    conn.privmsg(event.target, "I am a IRC bot programmed in Python using python-irc and using irc.glados.tv. I was made by Ryan 'obnoxious' Brogan aka http://twitter.com/awful")

def cmd_join(conn, event):
    config = json.loads(open('config.json', 'r').read())
    channelToJoin = event.arguments[0].split()[1].lower()
    if "#%s"%channelToJoin not in config['channels']:
        config['channels'].append("#%s"%channelToJoin)
        conn.join("#%s"%channelToJoin)
        config2 = open('config.json', 'w')
        config2.write(json.dumps(config))
        config2.close()
        conn.privmsg(event.target, "Joined: #%s"%channel)
        return
    else:
        conn.privmsg(event.target, "Already in: #%s.."%channelToJoin)
        return

def cmd_part(conn, event):
    config = json.loads(open('config.json', 'r').read())
    channelToPart = event.arguments[0].split()[1].lower()
    if "#%s"%channelToPart in config['channels']:
        config['channels'].remove("#%s"%channelToPart)
        conn.join("#%s"%channelToPart)
        config2 = open('config.json', 'w')
        config2.write(json.dumps(config))
        config2.close()
        conn.privmsg(event.target, "Parted: #%s"%channel)
        return
    else:
        conn.privmsg(event.target, "Already in: #%s.."%channelToPart)
        return

commandDict = {
    'join': cmd_join,
    'ping': cmd_ping,
    'say': cmd_say,
    'help': cmd_help,
    'about': cmd_about,
}