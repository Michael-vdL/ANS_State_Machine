#Driver for Inputing State Transitions and States
#!/usr/bin/python
import json

####
##BEFORE LEAVING PYCHARM TESTING ENVIRONMENT SET INPUT TO raw_input
####

#Prototype for how writing modular states and transitions could work
#1.) Takes in user input for states they would like to add
#2.) Tales in user input for name of state they would like to transition to
#3.) Takes in user input for rules that they would like to assign for transitions
def get_state_input():
    state_dict = {}
    print("#################################")
    print("Welcome to State Generation")
    print("#################################")
    adding_state = True
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

