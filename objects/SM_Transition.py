# Used to make Transitions Global
# Holds a transition code, used in swap management and destination state for transition
# !/usr/bin/python

from api.triggers.new_entity_triggers import trigger_handler

class Transition:
    def __init__(self, trans_name, trans_destination, trans_trigger):
        self.name = trans_name
        self.destination = trans_destination
        self.trigger = trans_trigger

    # Checks if a specific node has triggered a transition
    def check_trigger(self, node):
        return trigger_handler(self.trigger, node)

    # Takes in a state, and a list of nodes that triggered transitions
    def transition_nodes(self, start_state, node_list):
        for node in node_list:
            print("Running Transition on {} from {} to {}".format(node.name, start_state.name, self.destination.name))
            self.run_transition(start_state, node)

    # Runs a transition by taking in the nodes start state and the node
    def run_transition(self, start_state, node):
        # Remove Node from Start_State
        start_state.remove_node(node)
        # Add Node to New State
        self.destination.add_node(node)
