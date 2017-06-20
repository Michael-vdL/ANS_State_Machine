# Driver for Modifying States
#!/usr/bin/python
import json

####
##BEFORE LEAVING PYCHARM TESTING ENVIRONMENT SET INPUT TO raw_input
####

#Prototype for how writing modular states and transitions could work
#1.) Takes in user input for states they would like to add
#2.) Tales in user input for name of state they would like to transition to
#3.) Takes in user input for rules that they would like to assign for transitions

# Branch, Updates, Date
# Branch = Modular Functionality, Update = Redesign of State Class called for a redesign of the state maker. Reworked the way it requested input, added requests to match new parameters 6.20.17

# Takes in Current State Dictionary(For Validity Testing) Outputs Updated Dictionary with Valid States
def get_state_input(current_state_dict):
    state_dict = {}  #Makes a fresh dictionary to edit
    print("#################################")
    print("Welcome to State Editor")
    print("#################################")
    choice = input("What would you like to do? (New, Cancel, Edit, Remove, No Save: ")

    adding_state = choice.lower()  # Forces lower_case on string, hopefully reducing input errors

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

        # Input Section
        state_name = input("Please enter the name of the State you would like to add: ")
        # Add Check for if State Name Already Exists
        state_type = input("Please Enter the type of state you would like to add (start, end, normal): ")

        # Add Check for if there is already a Start State
    elif choice == 'edit':
    else:
        print("Sorry, that's not an option.")
        state_dict.update(current_state_dict)
        return get_state_input(state_dict)
    while adding_state:
        state_name = raw_input("Please enter the name of the State you would like to add(if done, enter done): ")
        if state_name == 'done':
            adding_trans=False
            adding_state = False
        else:
            adding_trans = True
            trans_list = []
        while adding_trans:
            to_state = raw_input("Please enter the name of the State you would like to allow transitions to(if done, enter done): ")
            if to_state == 'done':
                update_dict = {state_name : trans_list}
                state_dict.update(update_dict)
                adding_trans = False
            else:
                trans_list.append(to_state)
        if not adding_state:
            print("#################################")
            print("Leaving from State Generation")
            print("#################################")
            return state_dict

def get_transition_input():
    trans_dict = {}
    print("#################################")
    print("Welcome to Transition Generation")
    print("#################################")
    adding_trans = True
    while adding_trans:
        trans_code = raw_input("Please enter the code for your transition(if done, enter done): ")
        if trans_code == 'done':
            adding_trans = False
            return trans_dict
        else:
            desination_state = raw_input("Please enter the destination for your transition: ")
            update_dict = {trans_code : desination_state}
            trans_dict.update(update_dict)

