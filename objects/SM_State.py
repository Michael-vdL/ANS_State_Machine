#Class for States
#Takes in load data (state_name, trans_perm_list) --> See SM_File_Loader.py

# !/usr/bin/python

class State(object):
    def __init__(self, state_name, state_type, trans_list, function_list):
        # Static State Variables
        self.name = state_name  # Reference Name for State
        self.type = state_type  # For assigning Start(Idea : Device Discorvery State) or End(Idea : Device Removal State)
        self.trans = trans_list  # Permissions for Transitions from state. Allow transitions to be global
        self.funcs = function_list  # Permissions for Functions this state has access to
        # Dynamic Variables
        self.nodes_in_state = []
        self.nodes_to_swap = {}

    #node management
    # 1.) add_Node
    #2.) remove_node
    def add_node(self, node):
        self.nodes_in_state.append(node)

    def remove_node(self, node):
        print(node)
        self.nodes_in_state.remove(node)

    # node transistions
    def remove_permissions(self, node):
        print("Placeholder - Removed Permissions")

    def add_transitions(self, node):
        print("Placeholder - Add Permissions")
