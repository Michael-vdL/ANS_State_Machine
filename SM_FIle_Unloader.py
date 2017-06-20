#Writing Driver for Prototype
#!/usr/bin/python
import json

from SM_File_Loader import *

def on_write(state_dict, trans_dict, update_dict):
    current_components = on_load('states.txt', 'transitions.txt', 'update.txt')
    updated_state_dict = state_dict.update(current_components[0])
    updated_trans_dict = state_dict.update(current_components[1])
    print("Writing States to states.txt")
    state_write(updated_state_dict)
    print("Writing Transitions to transitions.txt")
    trans_write(updated_trans_dict)
    print("Writing Updates to update.txt")

def state_write(state_dict):
    with open('states.txt', 'w') as outfile:
        json.dump(state_dict, outfile)

def trans_write(trans_dict):
    with open('transitions.txt', 'w') as outfile:
        json.dump(trans_dict, outfile)
