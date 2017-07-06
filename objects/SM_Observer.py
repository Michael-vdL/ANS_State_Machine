#!/usr/bin/python

from objects.SM_State import *
from objects.SM_Transition import *
from objects.SM_Node import *


def get_dict(file_name):
    import json
    with open('resources/{}.txt'.format(file_name)) as resource_file:
        dict = json.load(resource_file)
    return dict

class Observer:
    def __init__(self):
        # Initial Observer Setup
        self.states, self.transitions = self.network_objects()
        # Saves Nodes
        self.node_location_dict = {}
        for state in self.states:  # Goes through each state in observer
            temp_dict = {
                state.name: state.nodes_in_state}  # makes an entry with the states name, and the nodes in the state
            self.node_location_dict.update(temp_dict)  # adds said entry

    # Refresh Function for network objects
    def get_network_objects(self):
        self.states, self.transitions = self.network_objects()  # Refreshes objects
        for state in self.states:  # Goes through each state
            for state_name in self.node_location_dict:  # Goes through the node_location_dictionary
                if state_name == state.name:  # If the state had node before the refresh
                    state.nodes_in_state = self.node_location_dict[state_name]  #Add them back into the state

    def network_objects(self):
        # Get Dictionary Data
        states_dict = get_dict('states')
        trans_dict = get_dict('transitions')
        # Make States
        state_list = self.state_objects(states_dict)
        # Make Transitions
        trans_list = self.transition_objects(trans_dict, state_list)

        return state_list, trans_list

    def state_objects(self, states_dict):
        # Functionality: Make State Objects, add them to a list
        state_list = []
        for state_name in states_dict:
            current_state = states_dict[state_name]
            state_type = current_state['type']
            state_trans = current_state['trans_perms']
            state_funcs = current_state['func_perms']
            state_obj = State(state_name, state_type, state_trans, state_funcs)
            state_list.append(state_obj)
        return state_list

    def transition_objects(self, trans_dict, state_list):
        trans_list = []
        for trans_name in trans_dict:
            current_trans = trans_dict[trans_name]
            trans_dest = current_trans['dest']
            for state in state_list:
                if state.name == trans_dest:
                    trans_state = state
            trans_func = current_trans['func']
            trans_obj = Transition(trans_name, trans_state, trans_func)
            trans_list.append(trans_obj)
        return trans_list

    def run_transition(self, start_state, node, transition):
        print("Possibly 1")
        destination_state = transition.destination
        print("Possibly 2")
        start_state.remove_node(node)
        print("Possibly 3")
        destination_state.add_node(node)
        print("Possibly 4")




"""""
class Observer:
    def __init__(self, name, component_list, mininet_network):
        #Configuring Observer from files/driver
        self.name = name
        self.state_dict = {}
        self.trans_list = []
        self.components = component_list
        self.get_components()
        self.net = mininet_network
        self.find_nodes()
        #Temp Structure for simulating updating JSON
        self.update_log = []
        self.net.start()

    #Methods that keep Observer up-to-date and output useful information
    #0.) Get Components
    def get_components(self):
        for state in self.components[0]:
            update_dict = {state : 0}
            self.state_dict.update(update_dict)
        for trans in self.components[1]:
            self.trans_list.append(trans)

    #1.) Find New Devices
    def find_nodes(self):
        node_list = self.net.keys()
        start_state = None
        for state in self.state_dict:
            if state.is_start:
                start_state = state
        if start_state:
            for node in node_list:
                start_state.add_node(node)
        else:
            print("Please next time designate a start state")

    #2.) Find Nodes in State
    def state_check(self):
        for state in self.state_dict:
            for node in state.nodes_in_state:
                print("Node: "+node+" in State: "+state.name)

    #3.) Updates Node Count for Observer State_Dict
    def update_state_dict(self, state):
        n_in_state = len(state.nodes_in_state)
        update_dict = {state: n_in_state}
        self.state_dict.update(update_dict)
        print("Nodes in State: " + state.name +" = " + str(self.state_dict[state]))

    #Transition Management Method
    def run_transitions(self):
        for state in self.state_dict:
            for node in state.nodes_to_swap:
                swap_code = state.nodes_to_swap[node]
                for trans in self.trans_list:
                    if swap_code == trans.code:
                        state.remove_node(node)
                        for d_state in self.state_dict:
                            if d_state.name == trans.destination:
                                d_state.add_node(node)
                                print("Transition: Node - " + node + ": " + state.name + " --> " + d_state.name)
            state.nodes_to_swap.clear()

    #Will be constant operating method for observer
    def listening(self):
        is_listening = True
        while is_listening:
            print("Observer is Listening for Updates")
            if len(self.update_log) > 0:
                self.handle_update()
            else:
                is_listening = False
            self.run_transitions()


    #For purposes of this demonstration, this method only recieves a node, not what kind of update (This is for security example)
    def handle_update(self):
        update = self.update_log.pop()
        for state in self.state_dict:
            if state.nodes_in_state.__contains__(update):
                print("Host found in State: "+state.name)
                state.mark_unhealthy(update)

    def test_transition(self):
        for state in self.state_dict:
            if state.is_start:
                state.mark_new()
    #Temp way to modularize stopping mn
    def net_stop(self):
        self.net.stop()

"""""
