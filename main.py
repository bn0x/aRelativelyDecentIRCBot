import sys
import json
import commands
import threading
import irc.bot
import irc.strings
from irc.bot import ServerSpec
from irc.client import ip_numstr_to_quad
from irc.client import ip_quad_to_numstr
from time import gmtime
from time import strftime
from time import sleep

class AwfulBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, password, port):
        spec = ServerSpec('irc.glados.tv', 6667, password)
        irc.bot.SingleServerIRCBot.__init__(self, [spec], nickname, nickname)
        self.channelsToJoin = channels

    def on_nicknameinuse(self, conn, event):
        sys.exit("Username is in use, weird.")

    def on_welcome(self, conn, event):
        threading.Thread(target=self.timedRehash).start()
        self.rehash()
        self.log('Connected')
        for channel in self.channelsToJoin:
            conn.join(channel)

    def on_privmsg(self, conn, event):
        conn.privmsg(event.source.nick, "I only work in channels, sorry!")

    def on_pubmsg(self, conn, event):
        if event.arguments[0].startswith("!"):
            command = event.arguments[0].split()[0].split('!')[1]
            if "rehash" in command:
                self.rehash()
                self.log("Rehashing..")
                conn.privmsg(event.target, "Rehashed")
                return
            else:
                pass

            self.log('Received: !%s command'%command)

            try:
                self.log('Processing %s..'%command)
                self.commands[command](conn, event)
            except:
                self.log('Exception')
                conn.privmsg(event.target, "Error running: !%s"%command)
                self.log('Error running: !%s'%command)

    def on_join(self, conn, event):
        self.log("Joined %s"%event.target)

    def do_command(self, event, cmd):
        nick = event.source.nick
        c = self.connection

    def log(self, message):
        print("%s [+] %s" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), message))

    def rehash(self):
        reload(commands)
        self.commands = commands.commandDict

    def timedRehash(self):
        while True:
            try:
                self.rehash()
                sleep(3)
            except:
                self.log("Rehashing is hard.")

class main(object):
    config = json.loads(open('config.json', 'r').read())
    bot = AwfulBot(config['channels'], config['nick'], config['server'], config['pass'], config['port'])
    bot.start()

if __name__ == "__main__":
    main()