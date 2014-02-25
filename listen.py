import driver
import time
from datetime import datetime
from pprint import pprint

#=============================================================================

readbuffer = ''
FILES_WRITTEN_TODAY = 0
LINES_WRITTEN_TO_FILE = 0
DATE = str(datetime.now()).split()[0]

SYSTEM_TIME = time.time()
UNIT_TIME = 5  # seconds

SWEARS_PER_UNIT_TIME = 0
CAPS_PER_UNIT_TIME = 0
TOTAL_PER_UNIT_TIME = 0

MAX_LINES_PER_FILE = 100

#=============================================================================

s = driver.connect()

fname = driver.getFileName(FILES_WRITTEN_TODAY, DATE)
f = open(fname, "w")

shitlist = set([word.strip().lower() for word in open('swearwords.txt')])
ignorelist = ['a', 'b', 'start', 'up', 'down', 'left', 'right']

while (True):

    readbuffer = s.recv(1024).decode("UTF-8", errors="ignore")

    for msg in readbuffer.split('\n'):
        m = driver.Message(msg)

        if (m.sender == None):
            continue

        else:
            TOTAL_PER_UNIT_TIME += 1

            if (time.time() >= SYSTEM_TIME + UNIT_TIME):
                print( "Swears per unit time: {}".format(SWEARS_PER_UNIT_TIME) )
                print( "CAPS   per unit time: {}".format(CAPS_PER_UNIT_TIME) )
                print( "TOTAL  per unit time: {}".format(TOTAL_PER_UNIT_TIME) )
                print("--")
                SYSTEM_TIME = time.time()
                SWEARS_PER_UNIT_TIME = 0
                CAPS_PER_UNIT_TIME = 0
                TOTAL_PER_UNIT_TIME = 0

            if (m.isIgnored(ignorelist)):
                continue

            if ( m.isSwear(shitlist) ):
                print(m)
                SWEARS_PER_UNIT_TIME += 1

            #elif maybe
            if ( m.isAllCaps() ):
                print(m)
                CAPS_PER_UNIT_TIME += 1



            #print("{} {} {}\n".format(m.time, m.sender, m.contents))
