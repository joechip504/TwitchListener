import driver
import time
from datetime import datetime
from pprint import pprint
from random import randint as ri
from chunkarray import Chunk, ChunkArray

#=============================================================================

readbuffer = ''
FILES_WRITTEN_TODAY = 0
LINES_WRITTEN_TO_FILE = 0
DATE = str(datetime.now()).split()[0]

UNIT_TIME = 3  # seconds

# THIS NEEDS TO BE FIXED
SYSTEM_TIME = time.time()
SWEARS_PER_UNIT_TIME = 0
CAPS_PER_UNIT_TIME = 0
TOTAL_PER_UNIT_TIME = 0
MAX_LINES_PER_FILE = 1000

FUTURE = time.time() + 2.5 * 60 + ri(0, 60)

#=============================================================================

s = driver.connect()

fname = driver.getFileName(FILES_WRITTEN_TODAY, DATE)
f = open(fname, "a")

shitlist = set([word.strip().lower() for word in open('swearwords.txt')])
ignorelist = ['a', 'b', 'start', 'up', 'down', 'left', 'right']

recent_chat = ChunkArray()

while (True):

    # send a message every 2-3 minutes to try and stay connected
    # to chat
    if (time.time() >= FUTURE):
        driver.chat(s)
        FUTURE = time.time() + 2.5 * 60 + ri(0, 60)

    # maybe this is where the bottleneck is? Test later
    readbuffer = s.recv(1024).decode("UTF-8", errors="ignore")

    for msg in readbuffer.split('\n'):
        m = driver.Message(msg)

        if (m.sender == None):
            continue

        else:
            TOTAL_PER_UNIT_TIME += 1

            if (LINES_WRITTEN_TO_FILE >= MAX_LINES_PER_FILE):
                f.close()
                FILES_WRITTEN_TODAY += 1
                LINES_WRITTEN_TO_FILE = 0

                # check if it's a new day too; will add later
                new_fname = driver.getFileName(FILES_WRITTEN_TODAY, DATE)
                f = open(new_fname, "a")

            if (time.time() >= SYSTEM_TIME + UNIT_TIME):
                C = Chunk(CAPS_PER_UNIT_TIME, SWEARS_PER_UNIT_TIME,
                          TOTAL_PER_UNIT_TIME)

                print("%.2f percent" % (100 * recent_chat.flagged()))
                recent_chat.push(C)

                f.write(str(C))
                LINES_WRITTEN_TO_FILE += 1

                SYSTEM_TIME = time.time()
                SWEARS_PER_UNIT_TIME = 0
                CAPS_PER_UNIT_TIME = 0
                TOTAL_PER_UNIT_TIME = 0

            if (m.isIgnored(ignorelist)):
                continue

            if (m.isSwear(shitlist)):
                SWEARS_PER_UNIT_TIME += 1

            elif (m.isAllCaps()):
                CAPS_PER_UNIT_TIME += 1

            #print("{} {} {}\n".format(m.time, m.sender, m.contents))
