# Main File For All State Machine Editing Functionality
# Will Contain:
# 0.) Grabs Resources on Call
# 1.) State Editor Function Calls
# 2.) Transition Editor Function Calls
# 3.) Read and Write Function Calls

from workshop.SM_State_Editor import *
from workshop.SM_Transition_Editor import *
from workshop.SM_Builder import *


def workshop_intro():
    resources = get_resources()
    print("#################################")
    print("Welcome to State Machine Workshop - ")
    print("#################################")
    print("...Gathering Resources...")
    if resources:
        print("{} Resources Were Found".format(len(resources)))
        # Editing Options
        workshop_setup()
    else:
        # Initial Setup
        # Segment for Error Checking System w/o resources
        print("No Resources Found - ")
        print("...Error Loading Resources or First Time Setup...")
        return


def workshop_setup():
    # Segment for Selecting Editing Mode
    print("#################################")
    choice = input("Please Select a Resource to Edit(States, Transitions, Validity, Done): ")
    print("#################################")
    choice = choice.lower()
    if choice == 'done':
        print("...Leaving Workshop Editor...")
        return
    elif choice == 'states':
        current_dict = get_state_dict()
        start_dict = get_state_dict()
        new_dict = workshop_state_editor(current_dict, start_dict)
        save_state_dict(new_dict)
        return workshop_setup()
    elif choice == 'transitions':
        current_dict = get_trans_dict()
        start_dict = get_trans_dict()
        new_dict = workshop_transition_editor(current_dict, start_dict)
        save_trans_dict(new_dict)
        return workshop_setup()
    elif choice == 'validity':
        state_dict = get_state_dict()
        trans_dict = get_trans_dict()
        sm_validity(state_dict, trans_dict)
        return workshop_setup()
    else:
        print("Sorry that is not an option. Please try again.")
        return workshop_setup()


# Gets all the files in resource directory
def get_resources():
    from os import listdir
    resource_list = [file for file in listdir('resources')]
    return resource_list

# Converts JSON to dictionary for editing
def get_state_dict():
    import json
    with open('resources/states.txt') as state_file:
        state_dict = json.load(state_file)
    return state_dict

def get_trans_dict():
    import json
    with open('resources/transitions.txt') as trans_file:
        trans_dict = json.load(trans_file)
    return trans_dict

# Converts Dict to JSON for saving
def save_state_dict(saving_dict):
    with open('resources/states.txt', 'w') as outfile:
        json.dump(saving_dict, outfile)

def save_trans_dict(saving_dict):
    with open('resources/transitions.txt', 'w') as outfile:
        json.dump(saving_dict, outfile)
