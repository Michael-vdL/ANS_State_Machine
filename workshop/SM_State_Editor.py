# Driver for Modifying States
# !/usr/bin/python
import json


####
##BEFORE LEAVING PYCHARM TESTING ENVIRONMENT SET INPUT TO raw_input
####

# Prototype for how writing modular states and transitions could work

# Functionality Not in Place:
# 1.) Edit --> In Place as of v_0.3
# 2.) Remove --> In place as of v_0.3
# 3.) Error Handling

# Branch, Updates, Date
# Branch = Modular Functionality, Update = Redesign of State Class called for a redesign of the state maker. Reworked the way it requested input, added requests to match new parameters 6.20.17

# Takes in Current State Dictionary(For Validity Testing) Outputs Updated Dictionary with Valid States

def workshop_state_editor(current_state_dict, start_state_dict):
    state_dict = {}  # Makes a fresh dictionary to edit
    print("#################################")
    print("Welcome to State Editor")
    print("#################################")
    choice = input("What would you like to do? (New, Edit, Remove, List, Exit, No Save): ")
    choice = choice.lower()  # Forces lower_case on string, hopefully reducing input errors

    # To Leave State Creation
    if choice == 'exit':
        # Functionality:
        # Exits State Creation and Saves Changes
        print("...Leaving State Editor - w/ Save... ")  # Simple Print Warning
        state_dict.update(current_state_dict)  # Adds Previous States to the State Dict
        return state_dict  # Desired Exit Strategy --> Returns Updated Dictionary to Write to JSON

    elif choice == 'no save':
        # Functioanlity:
        # 1.) Returns start_state_dict --> Stores with each pass so changes don't get applied
        print("...Leaving State Editor - w/o Save...")
        return start_state_dict

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
        return workshop_state_editor(state_dict, start_state_dict)

    elif choice == 'edit':
        # Functionality:
        # 1.)Input a State Name --> Checks to make sure state exits --> Bonus: Asks if you would like to make a new state with that name
        # 2.)Allow Editing Name --> Checks to make sure new name doesn't already exist
        # 3.)Allow Editing Type --> Checks to make sure no state is already a start state --> Bonus: Asks if you would like to override that states functionality
        # 4.)Allow Editing Function Permissions
        # 5.)Allow Ediiting State Transfer Permissions

        # Calls Function, Updates Dict, Recalls State Editor With New Dictionary
        state_dict = edit_state(current_state_dict, None)
        return workshop_state_editor(state_dict, start_state_dict)

    elif choice == 'remove':
        # Functionality:
        # Removes Selected State From Dict
        state_dict = remove_state(current_state_dict)
        return workshop_state_editor(state_dict, start_state_dict)
        #Error Check: State Existence

    elif choice == 'list':
        # Functionality:
        # List the Current States in the Dictionary
        list_state(current_state_dict)
        return workshop_state_editor(current_state_dict, start_state_dict)


    else:
        print("Sorry, that's not an option.")
        state_dict.update(current_state_dict)
        return workshop_state_editor(state_dict, start_state_dict)


###########################################
# Function Group For Options
###########################################

def new_state():
    # 1.)Input a State Name
    state_name = input("Please enter the name of the State you would like to add: ")
    # Error Check: Check if state Already Exists
    # 2.)Input a State Type
    state_type = input("Please Enter a type (start, end, normal): ")
    # Error Check: if Start, check if only start
    # 3.)Input Function Permissions
    state_functions = input(
        "Please Enter the Functions you would like to give this state has access to(seperated by commas, ex. enter,mark): ")
    state_functions = state_functions.replace(' ', '')
    state_functions = state_functions.split(',')
    # 4.)Input Transfer Permissions
    state_transfer = input("Please Enter the Transitions this state has access t(seperated by comas): ")
    state_transfer = state_transfer.replace(' ', '')
    state_transfer = state_transfer.split(',')
    print("...Adding New State: {}...".format(state_name))
    return {state_name: {'type': state_type, 'func_perms': state_functions, 'trans_perms': state_transfer}}


def edit_state(current_state_dict, name):
    # 1.)Input a State Name
    if not name:
        state_name = input("Please enter the name of the State you would like to edit(list to view list of states): ")
        # Error Check: Existance Check
        return edit_state(current_state_dict, state_name)
    elif name == 'list':
        # Calling the List Function
        list_state(current_state_dict)
        return edit_state(current_state_dict, None)
    elif not current_state_dict.__contains__(name):
        print("Sorry that Name Does Not Exist, Please Try Again")
        return edit_state(current_state_dict, None)
    else:
        state_name = name
        state_dict = current_state_dict
        editing_state = state_dict.pop(state_name)  # Takes Dict Value for State Name
        choice = input("What Property would you like to Edit(Name, Type, Functions, Transitions, Done): ")
        choice = choice.lower()

        if choice == 'done':
            print("...Finished Editing State: {}...".format(state_name))
            update_dict = {state_name: editing_state}
            state_dict.update(update_dict)
            return state_dict
        # 2.)Input for New Name
        elif choice == 'name':
            new = input("Enter new Name for State: ")
            update_dict = {new: editing_state}
            state_dict.update(update_dict)
            return edit_state(state_dict, new)
        # 3.)Input for New Type
        elif choice == 'type':
            new = input("Enter new Type for State: ")
            editing_state['type'] = new
            update_dict = {state_name: editing_state}
            state_dict.update(update_dict)
            return edit_state(state_dict, state_name)
        # 4.)Input for New Function Perms
        elif choice == 'functions':
            new = input("Enter new Function Permisions for State: ")
            new = new.replace(' ', '')
            new = new.split(',')
            editing_state['func_perms'] = new
            update_dict = {state_name: editing_state}
            state_dict.update(update_dict)
            return edit_state(state_dict, state_name)
        # 5.) Input for New Transition Perms
        elif choice == 'transitions':
            new = input("Enter new Transitions for State: ")
            new = new.replace(' ', '')
            new = new.split(',')
            editing_state['trans_perms'] = new
            update_dict = {state_name: editing_state}
            state_dict.update(update_dict)
            return edit_state(state_dict, state_name)
        else:
            print("That is not one of the options, please try again.")
            return edit_state(current_state_dict, state_name)


def remove_state(state_dict):
    remove_state_dict = state_dict
    # 1.) Input a State Name
    state_name = input("Please enter the name of the State you would like to remove(list to view list of states): ")
    # Error Check: State Must Exist
    if state_name == 'list':
        list_state(state_dict)
        return remove_state(state_dict)
    elif not state_dict.__contains__(state_name):
        print("Sorry, that state does not exist, please try again.")
        return remove_state(state_dict)
    else:
        remove_state_dict.pop(state_name)
        print("...Removing State: {}...".format(state_name))
        return remove_state_dict


def list_state(state_dict):
    # Lists States and their Properties
    if len(state_dict) == 0:
        print("...No States to List...")
        return
    else:
        counter = 1
        for state_name in state_dict:
            state = state_dict[state_name]
            print("{}.) {} - Type: {} | Functions: {} | Transitions: {}".format(counter, state_name, state['type'],
                                                                                state['func_perms'],
                                                                                state['trans_perms']))
            counter += 1
        return


#########################################
# Function Group For Error Checks

def edit_state_error_check():
    return
