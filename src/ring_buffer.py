class RingBuffer:
    """ class that implements a not-yet-full buffer """

    def __init__(self, size_max):
        self.max = size_max
        self.data = []
        self.cur = 0

    def _full_append(self, x):
        """ Append an element overwriting the oldest one. """
        self.data[self.cur] = x
        self.cur = (self.cur+1) % self.max

    def _full_get(self):
        """ return list of elements in correct order """
        return self.data[self.cur:]+self.data[:self.cur]

    def append(self, x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:

            # Replace the get/append methods
            self.append = self._full_append
            self.get = self._full_get

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data