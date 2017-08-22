#Class for States
#Takes in load data (state_name, trans_perm_list) --> See SM_File_Loader.py

# !/usr/bin/python

from api.junos import junos_api as j_api
from api.triggers import *


class State(object):
    def __init__(self, state_name, state_type, trans_list, function_list):
        # Static State Variables
        self.name = state_name  # Reference Name for State
        self.type = state_type  # For assigning Start(Idea : Device Discorvery State) or End(Idea : Device Removal State)
        self.trans = trans_list  # Permissions for Transitions from state. Allow transitions to be global
        self.funcs = function_list  # Permissions for Functions this state has access to
        self.transition_objects = []
        # Dynamic Variables
        self.nodes_in_state = []
        self.orphans_in_state = []

    #node management
    # 1.) add_Node
    #2.) remove_node
    def add_node(self, node):
        #self.enter_routine(node)
        node.current_state = self
        if not node.parent:
            self.parent_arrived(node)
            self.nodes_in_state.append(node)
        elif self.nodes_in_state.__contains__(node.parent):
            self.nodes_in_state.append(node)
        else:
            self.orphans_in_state.append(node)

    def remove_node(self, node):
        #self.exit_routine(node)
        if not node.parent:
            self.parent_left(node)
            self.nodes_in_state.remove(node)
        elif self.orphans_in_state.__contains__(node):
            self.orphans_in_state.remove(node)
        else:
            self.nodes_in_state.remove(node)

    def parent_arrived(self, parent_node):
        children_of_parent = []
        for node in self.orphans_in_state:
            if node.parent is parent_node:
                children_of_parent.append(node)
        for child in children_of_parent:
            self.nodes_in_state.append(child)
            self.orphans_in_state.remove(child)

    def parent_left(self, parent_node):
        children_of_parent = []
        for node in self.nodes_in_state:
            if node.parent is parent_node:
                children_of_parent.append(node)
        for child in children_of_parent:
            self.nodes_in_state.remove(child)
            self.orphans_in_state.append(child)

    # node transistions
    def get_transition_objects(self, trans_list):
        for trans_obj in trans_list:
            for trans_name in self.trans:
                if trans_obj.name == trans_name:
                    self.transition_objects.append(trans_obj)

    def check_transition_triggers(self):
        trigger_count = 0
        for transition in self.transition_objects:
            nodes_to_transition = []
            for node in self.nodes_in_state:
                if transition.check_trigger(node):
                    trigger_count += 1
                    nodes_to_transition.append(node)
            transition.transition_nodes(self, nodes_to_transition)
        print("Nodes for {} all Checked - {} were hit.".format(self.name, trigger_count))



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
