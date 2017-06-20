#Class for States
#Takes in load data (state_name, trans_perm_list) --> See SM_File_Loader.py

class State(object):
    def __init__(self, state_name, trans_perm_list):
        #Reference Name for State
        self.name = state_name
        #Permissions for Transitions from state. Allow transitions to be global
        self.perms = trans_perm_list
        #Private variables for managing nodes in state
        self.nodes_in_state = []
        self.nodes_to_swap = {}
        self.is_start = False
        if state_name == 'start':
            self.is_start = True

    #node management
    def add_node(self, node):
        self.nodes_in_state.append(node)

    def remove_node(self, node):
        self.nodes_in_state.remove(node)

    #transition management
    def add_transition_perm(self, to_state):
        self.perms.append(to_state)

    def remove_trans_perm(self, to_state):
        self.remove_trans_perm(to_state)

    #Transition Management Methods
    #adds nodes to the states swap list, and labels them for the observer to swap
    def designate_swap(self, node, swap_code):
        if self.check_valid_swap(swap_code):
            update_dict = {node : swap_code} #Creates a single entity dict to update the nodes to swap
            self.nodes_to_swap.update(update_dict)
        else:
            print("Invalid Transition: Check State Transition Permission Properties")
    #Simply check if the state is allowed to make the transition that is being requested
    #Most likely will never be hit but I figure its best to be safe than sorry
    def check_valid_swap(self, swap_code):
        for perm in self.perms:
            if perm == swap_code:
                return True
            else:
                return False

    #This is the next thing to modularize
    def mark_new(self):
        for node in self.nodes_in_state:
            self.designate_swap(node, 'to_new')

    def mark_unhealthy(self, node):
        self.designate_swap(node, 'to_unhealthy')

#Used to make Transitions Global
#Holds a transition code, used in swap management and destination state for transition
class Transition:
    def __init__(self, trans_code, to_state):
        self.code = trans_code
        self.destination = to_state