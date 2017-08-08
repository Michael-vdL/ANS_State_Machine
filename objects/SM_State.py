#Class for States
#Takes in load data (state_name, trans_perm_list) --> See SM_File_Loader.py

# !/usr/bin/python

from api.junos import junos_api as j_api


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
        #self.enter_routine(node)
        self.nodes_in_state.append(node)

    def remove_node(self, node):
        #self.exit_routine(node)
        self.nodes_in_state.remove(node)

    # node transistions
    def remove_permissions(self, node):
        print("Placeholder - Removed Permissions")

    def add_transitions(self, node):
        print("Placeholder - Add Permissions")

    # Realms, Policy, Roles, Enforcement
    def enter_routine(self, node):
        print('Enforcing Enter Policy on {}'.format(node.name))
        # for func in self.funcs:
        # if func == 'interface_down':
        # self.interface_down(node)
        # elif func == 'get_policy':
        # j_api.api_handler(node, func)
        # elif func == 'check_health':
        # j_api.api_handler(node, func)

    def exit_routine(self, node):
        print('Enforcing Exit Policy on {}'.format(node.name))
        # for func in self.funcs:
        # if func == 'interface_up':
        # self.interface_up(node)

    # STATE FUNCS

    def interface_down(self, node):
        print('Node has entered Quarantine - Cutting Connection')
        j_api.disable_interface(node)

    def interface_up(self, node):
        print('Node has left Quarantine - Reenabling Connection')
        j_api.enable_interface(node)
