from enum import Enum


NUM_OF_STATES = 3


class State(Enum):
    OMW, HERE, NO = range(NUM_OF_STATES)

    def next(self):  # -> State
        """
        Get the next State in the cyclic order OMW -> HERE -> NO -> OMW
        :return: The following state
        """
        return State((self.value + 1) % NUM_OF_STATES)