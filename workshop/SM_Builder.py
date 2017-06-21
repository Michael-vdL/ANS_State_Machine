# Item that Drives Two Functions:
# 1)Builds the State Machine Object from resources
# 2)Runs State Machine Compile Check

from objects.SM_Observer import *
from objects.SM_State import *
from objects.SM_Transition import *


###########################################
# SM BUILDER
###########################################
def sm_builder(state_dict, trans_dict):
    # Steps:
    # 1.) Run Validity Check
    # 2.) Build Transitions
    # 3.) Build States
    # 4.) Build State_Machine
    # 5.) Profit

    # 1.) Validity Check
    if not sm_validity(state_dict, trans_dict):
        print("...SM is Invalid - Canceling Build...")
        return None
    else:
        print("...SM is Valid - Ready to Build...")
        # 2.) Build Transitions
        trans_list = transition_builder(trans_dict)
        state_list = state_builder(state_dict, trans_list)
        return Observer('Test', state_list, trans_list)


def transition_builder(trans_dict):
    # Functionality: Converts Dictionary Items to Transition Objects and returns a list
    trans_list = []
    for trans_name in trans_dict:
        trans = trans_dict[trans_name]
        trans_dest = trans['dest']
        trans_func = trans['func']
        obj_trans = Transition(trans_name, trans_dest, trans_func)
        trans_list.append(obj_trans)
    return trans_list


def state_builder(state_dict, trans_list):
    # Functionality: Converts Dictionary Items to State Objects and gives them access to transitions
    state_list = []
    for state_name in state_dict:
        state = state_dict[state_name]
        state_type = state['type']
        state_func = state['func_perms']
        state_trans_perms = state['trans_perms']  # To get name of transitions
        state_trans = []
        for perm in state_trans_perms:
            for trans in trans_list:
                if trans.name == perm:
                    state_trans.append(trans)
        obj_state = State(state_name, state_type, state_trans, state_func)
        state_list.append(obj_state)
    return state_list


###########################################
# SM COMPILER TEST
###########################################

def sm_validity(state_dict, trans_dict):
    # Steps:
    # 1.) Logic Check --> No Start state, No End state, Access to non-existant transitions, Transitions to non-existant states --> Returns False and provides warnings
    # 2.) Warnings Check  --> States that can't be reached --> Returns True but provides warning

    # 1.) Logic Checks
    if not logic_no_start_check(state_dict):
        print("Error with Start")
    elif not logic_no_end_check(state_dict):
        print("Error with End")
    elif not logic_unreachable_transition(state_dict, trans_dict):
        print("Error with Transitions")
    elif not logic_states_does_not_exist(state_dict, trans_dict):
        print("Error with State Existance")
    else:
        # 2.) Warning Checks
        print("...All SM Validity Checks Passed...")
        return True
    return False


###############
# SM Logic Tests
###############

def logic_no_start_check(state_dict):
    # Goes through each state --> if a state with type start is found, return true, if no state is found, return false
    for state_name in state_dict:
        state = state_dict[state_name]
        if state['type'] == 'start':
            print("...Start State Found: {}...".format(state_name))
            return True
    print("...No Start State Found...")
    return False


def logic_no_end_check(state_dict):
    # Goes through each state --> if a state with type end is found, return true, if no state is found, return false
    for state_name in state_dict:
        state = state_dict[state_name]
        if state['type'] == 'end':
            print("...End State Found: {}...".format(state_name))
            return True
    print("...No End State Found...")
    return False


def logic_unreachable_transition(state_dict, trans_dict):
    # Steps:
    # Goes through each state, gets list of transitions
    # Checks if each transition in list is contained in trans_dict
    for state_name in state_dict:
        state = state_dict[state_name]
        check_trans_list = state['trans_perms']
        if not all(trans in trans_dict for trans in check_trans_list):
            print("...Transition Unreachable in State: {}...".format(state_name))
            return False
    print("...No Unreachable Transitions...")
    return True


def logic_states_does_not_exist(state_dict, trans_dict):
    # Steps:
    # Goes through each transition, gets destination
    # Chekcs if state dict contains destination
    for trans_name in trans_dict:
        trans = trans_dict[trans_name]
        dest = trans['dest']
        if not state_dict.__contains__(dest):
            print("...Transition: {} attempted to reach non-existant State: {}".format(trans_name, dest))
            return False
    print("...No State Existance Issues...")
    return True

    ###########
    # SM Warning Checks
    ###########
    # Implementing Later
