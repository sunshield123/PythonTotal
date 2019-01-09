"""
Module has message object
"""


class Message(object):
    """
    Message class, need to maintain order in priority queue
    """

    def __init__(self, message,
                 sender,
                 message_id =1000000,
                 sequencer=None):
        """

        Args:
            message: message
            sender:  sender
            message_id: sequence id
            sequencer: sequencer
        """
        self.message = message
        self.sender = sender
        self.message_id = message_id
        self.sequencer = sequencer

    def __cmp__(self, other):
        return self.__lt__(other)

    def __lt__(self, other):
        if self.message_id < other.message_id:
            return True
        else:
            return False
