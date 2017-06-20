#Reading Driver for Prototype
#!/usr/bin/python
import json

from SM_Abstracts import *

def on_load(state_file, transition_file, update_file):
    state_list = load_states(state_file)
    transition_list = load_transitions(transition_file)
    update_list = load_update_json(update_file)
    sm_components = [state_list, transition_list]
    if state_list:
        print("States Loaded")
    else:
        print("Error Loading States")
    if transition_list:
        print("Transitions Loaded")
    else:
        print("Error Loading Transitions")
    if load_update_json(update_file):
        print("Updates Loaded")
    else:
        print("Error Loading Updates")
    return sm_components

def load_states(state_file):
    state_list = []
    with open(state_file) as state_f:
        data = json.load(state_f)
        for state in data:
            current_state = State(state, data[state])
            state_list.append(current_state)
    return state_list

def load_transitions(transition_file):
    transition_list = []
    with open(transition_file) as trans_f:
        data = json.load(trans_f)
        for trans in data:
            current_trans = Transition(trans, data[trans])
            transition_list.append(current_trans)
    return transition_list

def load_update_json(update_file):

    return True