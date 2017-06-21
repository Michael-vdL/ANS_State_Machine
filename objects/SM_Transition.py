# Used to make Transitions Global
# Holds a transition code, used in swap management and destination state for transition

class Transition:
    def __init__(self, trans_name, to_state, function):
        self.name = trans_name
        self.destination = to_state
        self.function = function
