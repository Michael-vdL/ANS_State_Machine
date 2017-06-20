# Driver for Modifying States
# !/usr/bin/python
import json


####
##BEFORE LEAVING PYCHARM TESTING ENVIRONMENT SET INPUT TO raw_input
####

# Prototype for how writing modular states and transitions could work
# 1.) Takes in user input for states they would like to add
# 2.) Tales in user input for name of state they would like to transition to
# 3.) Takes in user input for rules that they would like to assign for transitions

# Branch, Updates, Date
# Branch = Modular Functionality, Update = Redesign of State Class called for a redesign of the state maker. Reworked the way it requested input, added requests to match new parameters 6.20.17

# Takes in Current State Dictionary(For Validity Testing) Outputs Updated Dictionary with Valid States
def workshop_state_editor(current_state_dict):
    state_dict = {}  # Makes a fresh dictionary to edit
    print("#################################")
    print("Welcome to State Editor")
    print("#################################")
    choice = input("What would you like to do? (New, Cancel, Edit): ")

    choice = choice.lower()  # Forces lower_case on string, hopefully reducing input errors

    # To Leave State Creation
    if choice == 'cancel':
        print("...Leaving State Creation... ")  # Simple Print Warning
        state_dict.update(current_state_dict)  # Adds Previous States to the State Dict
        return state_dict  # Desired Exit Strategy --> Returns Updated Dictionary to Write to JSON
    elif choice == 'new':
        # Section for making New State
        # Functionality:
        # 1.)Input a State Name --> Checks to make sure no state like that already exists --> Bonus: Asks if you would like to edit that state instead
        # 2.)Input a State Type --> Checks to make sure no state is already a Start State --> Bonus: Asks if you would like to override that states functionality
        # 3.)Input a State Function Permissions --> Settings for Which Modular Functions to Enable
        # 4.)Input a State Transfers --> Settings for Which States This State Can Transfer To


        # Calls Function, Updates Dict, Recalls State Editor With New Dictionary
        state_dict.update(new_state())
        state_dict.update(current_state_dict)
        return workshop_state_editor(state_dict)

    elif choice == 'edit':
        # Functionality:
        # 1.)Input a State Name --> Checks to make sure state exits --> Bonus: Asks if you would like to make a new state with that name
        # 2.)Allow Editing Name --> Checks to make sure new name doesn't already exist
        # 3.)Allow Editing Type --> Checks to make sure no state is already a start state --> Bonus: Asks if you would like to override that states functionality
        # 4.)Allow Editing Function Permissions
        # 5.)Allow Ediiting State Transfer Permissions
        to_edit = input("Please Enter Name of State you would like to edit: ")

        return workshop_state_editor(state_dict)
    else:
        print("Sorry, that's not an option.")
        state_dict.update(current_state_dict)
        return workshop_state_editor(state_dict)


# Function Group For Options
###########################################
# New State Editor Group
def new_state():
    # 1.)Input a State Name
    state_name = input("Please enter the name of the State you would like to add: ")
    # Error Check: Check if state Already Exists
    # 2.)Input a State Type
    state_type = input("Please Enter a type (start, end, normal): ")
    # Error Check: if Start, check if only start
    # 3.)Input Function Permissions
    state_functions = input(
        "Please Enter the Functions you would like to give this state acccess to(seperated by commas, ex. enter,mark): ")
    state_functions = state_functions.strip()
    state_functions = state_functions.split(',')
    # 4.)Input Tranfer Permissions
    state_transfer = input("Please Enter the States this state can transfer to(seperated by comas): ")
    state_transfer = state_transfer.strip()
    state_transfer = state_transfer.split(',')
    return {state_name: {'type': state_type, 'func_perms': state_functions, 'trans_perms': state_transfer}}


def new_state_error_check():
    return

    ############################################
    # Edit State Editor Group


def edit_state():
    return


def edit_state_error_check():
    return
