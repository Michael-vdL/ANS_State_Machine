# Main File For All State Machine Editing Functionality
# Will Contain:
# 0.) Grabs Resources on Call
# 1.) State Editor Function Calls
# 2.) Transition Editor Function Calls
# 3.) Read and Write Function Calls

from workshop.SM_State_Editor import *


def workshop_setup():
    resources = get_resources()
    print("#################################")
    print("Welcome to State Machine Workshop - ")
    print("#################################")
    print("...Gathering Resources...")
    if resources:
        # Segment for Selecting Editing Mode
        print("{} Resources Were Found".format(len(resources)))
        choice = input("Please Select a Resource to Edit(States, Transitions): ")
        choice = choice.lower()
        if choice == 'states':
            current_dict = get_state_dict()
            new_dict = workshop_state_editor(current_dict, current_dict)
            save_state_dict(new_dict)
    else:
        # Segment for Error Checking System w/o resources
        print("No Resources Found - ")
        print("...Error Loading Resources or First Time Setup...")
        choice = input("Would you like to complete Setup?(Yes or No)")
        choice = choice.lower()
        if choice == 'no':
            print("Without Minimal Resources System Will Not Run - Must Complete one of the following: ")
            print("1.) Add Minimum Resources to resource directory (states.txt, transitions.txt)")
            print("2.) Complete Initial Setup")
            return
        elif choice == 'yes':
            print("Beginning Initial Setup: ")
        else:
            print("Sorry, It was a Yes or No Question, Please Try Again")
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


# Converts Dict to JSON for saving
def save_state_dict(saving_dict):
    with open('resources/states.txt', 'w') as outfile:
        json.dump(saving_dict, outfile)


if __name__ == '__main__':
    workshop_setup()
