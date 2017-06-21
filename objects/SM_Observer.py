#!/usr/bin/python

class Observer:
    def __init__(self, name, state_list, trans_list):
        self.name = name  # Probably useless variable, incase multiple observers become useful
        self.states = state_list  # List of states for observer
        self.transitions = trans_list  # List of transitions for observer

    def monitor_network_json(self):
        # Functionality: Monitors the network json for updates
        # 1.) Determines the nature of the update
        # 2.) Determines which state the update effects
        # 3.) Designates which function will handle the update
        return

    def get_network(self):
        # Functionality: Sets up a Mininet network for testing

        return

    def assign_new_node(self):
        # Funcationality: When new nodes are discovered it assigns them to start state.

        return

    def running(self):
        # Functionality: Controls everything the observer does
        # Currently a Manual Interactive method --> Will be automatic and controlled from elsewhere
        return


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
