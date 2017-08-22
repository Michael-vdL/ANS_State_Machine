import json
from jnpr.junos.utils.config import Config


def get_routine_dict():
    with open('resources/routines.json') as resource_file:
        dict = json.load(resource_file)
    return dict


def routine_handler(session, routine_call):
    routine_dict = get_routine_dict()
    return run_routine(session, routine_dict[routine_call])


def run_routine(session, routine_dict):
    conditions_list = routine_dict["condition_list"]
    input_list = routine_dict["input_list"]
    requested_input = get_requested_input(input_list)
    action_list = routine_dict["action_list"]

    # Add if statement for conditions

    with Config(session, mode='private') as cu:
        input_counter = 0
        for action in action_list:
            input_required = len([position for position, char in enumerate(action) if char == '*'])
            if input_required >= 1:
                action = action.replace("*", "{}")
                current_actions_input = []
                for i in range(input_required):
                    current_actions_input.append(requested_input[input_counter])
                    input_counter += 1
                cu.load(action.format(*current_actions_input))
            else:
                cu.load(action)
        cu.pdiff()
        cu.commit()


def get_requested_input(input_list):
    requested_input = []
    for input_request in input_list:
        response = input("Provide Input for {}:".format(input_request))
        requested_input.append(response)
    return requested_input


def edit_user_class():
    print("Edit User Class")
