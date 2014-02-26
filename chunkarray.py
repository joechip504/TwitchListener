class Chunk:

    """
    Represents data collected from a series of messages in one UNIT_TIME. 
    self.flagged: number of messages flagged as CAPS or swears. 
    self.messages:   total NUMBER of messages recieved. 
    NOT individual message contents.
    """

    def __init__(self, caps, swears, messages):
        self.flagged = caps + swears
        self.messages = messages

    def __str__(self):
        return "FLAGGED: {} OUT OF: {} MESSAGES\n".format(
            self.flagged, self.messages)


class ChunkArray:

    """
    Array of chunks. Calling add fills the array to 
    a specific size, then replaces the oldest element in the array

    self.alloc: number of chunks to allow in array. Not necessarily how
                many are currently contained.

    self.size: index of oldest element in self.data.
    self.data: list of chunks
    """

    def __init__(self, alloc=50):
        self.alloc = alloc
        self.size = 0
        self.data = []

    def full(self):
        """
        Returns True if the number of elements contained (self.size) is equal 
        to the number of spots allocated. Returns False otherwise.
        """
        return (len(self.data) == self.alloc)

    def push(self, i):
        """ add an element to the array """

        if (not self.full()):
            self.data.append(i)

        else:
            self.data[self.size] = i
            self.size += 1

            # after stepping through all of self.data, the oldest element is
            # at position 0
            if (self.size == self.alloc):
                self.size = 0

    def flagged(self):
        """ returns percentage of flagged messages """
        try:
            return sum([c.flagged for c in self.data]) / sum(
                [c.messages for c in self.data])

        except:
            return 0
