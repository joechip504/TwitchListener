import socket
import os
from datetime import datetime

#=============================================================================
# TWITCH INFORMATION HERE
#=============================================================================

HOST = "irc.twitch.tv"
PORT = 6667
AUTH = os.environ['TWITCHAUTH'] 
NICK = "joechip504"
IDENT = "joechip504"
REALNAME = "joechip504"
MASTER = "joechip504"

#=============================================================================

CHAT_CHANNEL = "joechip504"
#CHAT_CHANNEL = "twitchplayspokemon"

#=============================================================================


class Message:

    """ Represent data recieved from twitch more nicely. When I decide
    exactly this does, I'll update this thing """

    def __init__(self, buf):
        """ parse data from socket.recv """
        self.raw = buf
        self.time = str(datetime.now())

        # if data received is not a message, then we'll say it has no sender
        if (not isMessage(buf)):
            self.sender = None

        else:
            self.sender = buf.split("!")[0].strip(":")
            self.contents = buf.split(":")[-1].strip('\n')

    def __str__(self):
        return "{} {} {}".format(
                self.time, self.sender, self.contents)

    def isSwear(self, swearlist):
        """checks if the message contains a swear"""
        for word in self.contents.split():
            if word.lower() in swearlist:
                return True

        return False

    def isAllCaps(self):
        """checks if the message was typed in all caps"""
        return all( word.isupper() for word in self.contents.split() )

    def isIgnored(self, ignorelist):
        if (len( self.contents.split() ) == 1 and 
                self.contents.split()[0].lower() in ignorelist):
            return True

        return False

        



#=============================================================================
def _connect(HOST, PORT, AUTH, NICK, IDENT, REALNAME, MASTER, CHAT_CHANNEL):
    """ Establishes and returns connection to twitch.tv chat"""

    s = socket.socket()
    s.connect((HOST, PORT))

    s.send(bytes("PASS %s\r\n" % AUTH, "UTF-8"))
    s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
    s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
    s.send(bytes("JOIN #%s\r\n" % CHAT_CHANNEL, "UTF-8"))
    s.send(bytes("PRIVMSG #%s :Connected\r\n" % CHAT_CHANNEL, "UTF-8"))
    return s

#=============================================================================


def connect():
    """ CALL THIS FUNCTION """
    return _connect(HOST, PORT, AUTH, NICK, IDENT, REALNAME, MASTER, CHAT_CHANNEL)

#=============================================================================


def isMessage(buf):
    return ('PRIVMSG' in buf.split())

#=============================================================================


def getFileName(FILES_WRITTEN_TODAY, DATE):
    return "{}:{}.txt".format(DATE, FILES_WRITTEN_TODAY)

#=============================================================================

