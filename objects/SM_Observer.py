#!/usr/bin/python

from objects.SM_State import *
from objects.SM_Transition import *
from objects.SM_Node import *
from objects.SM_Network import *
from objects.junos.Junos_Node import *
from bin.junos_entity_generator import *
from bin.junos_information_collector import information_collector, configuration_collection
from api.routines.user_routines import routine_handler


def get_dict(file_name):
    import json
    with open('resources/{}.json'.format(file_name)) as resource_file:
        dict = json.load(resource_file)
    return dict

class Observer:
    def __init__(self):
        # Initial Observer Setup
        self.states, self.transitions = self.network_objects()
        self.device_session_status = {'open': [], 'closed': []}
        self.entity_dict = self.get_net_devices()
        self.assign_state_nodes()
        self.changes = []
        # Saves Nodes


    ######################################
    # Object Generation
    ######################################
    # Refresh Function for network objects
    def get_network_objects(self):
        self.states, self.transitions = self.network_objects()  # Refreshes objects
        self.assign_state_nodes()


    def network_objects(self):
        # Get Dictionary Data
        states_dict = get_dict('states')
        trans_dict = get_dict('transitions')
        # Make States
        state_list = self.state_objects(states_dict)
        # Make Transitions
        trans_list = self.transition_objects(trans_dict, state_list)
        for state in state_list:
            state.get_transition_objects(trans_list)
        return state_list, trans_list

    def state_objects(self, states_dict):
        # Functionality: Make State Objects, add them to a list
        state_list = []
        for state_name in states_dict:
            current_state = states_dict[state_name]
            state_type = current_state['type']
            state_trans = current_state['trans_perms']
            state_funcs = current_state['func_perms']
            state_obj = State(state_name, state_type, state_trans, state_funcs)
            state_list.append(state_obj)
        return state_list

    def transition_objects(self, trans_dict, state_list):
        trans_list = []
        for trans_name in trans_dict:
            current_trans = trans_dict[trans_name]
            trans_dest = current_trans['destination']
            trans_destination = None
            for state in state_list:
                if state.name == trans_dest:
                    trans_destination = state
            trans_trigger = current_trans['trigger']
            trans_obj = Transition(trans_name, trans_destination, trans_trigger)
            trans_list.append(trans_obj)
        return trans_list

    ############################################
    # Entity Generation
    ############################################

    # 1.) Gets All Devices:
    # 2.) Gets All Interfaces:
    # 3.) Gets All Users:

    def get_net_devices(self):  # Generate Junos Device Objects
        entity_dict = {}  # Used to Store Devices
        dev_list = gen_devices()  # Gets an Initial list of devices
        for junos_dev in dev_list:  # Goes through each device on the list
            self.device_session_status['closed'].append(junos_dev)
            dev_interfaces = self.get_dev_interfaces(junos_dev)  # Calls Method to collect all Interfaces for the Device
            dev_users = self.get_dev_users(junos_dev)
            tmp_dict = {junos_dev.name: {'dev_obj': junos_dev, 'interfaces': dev_interfaces, 'users': dev_users}}
            entity_dict.update(tmp_dict)
        return entity_dict

    def get_dev_interfaces(self, device):
        interfaces = gen_interfaces(device)
        return interfaces

    # Passes Device to user generator to make a list of objects
    # Gets list of user objects and makes sure to add them to the correct states
    def get_dev_users(self, device):
        users = gen_users(device)
        return users

    #################
    # Object Getter #
    #################

    def get_dev_by_name(self, search_name):
        for dev_name in self.entity_dict:
            if search_name == dev_name:
                device = self.entity_dict[dev_name]['dev_obj']
                return device

    def get_start_state(self):
        for state in self.states:
            if state.type == 'start':
                return state

    ############################################
    # Operational Functions
    ############################################
    def observe(self):
        # Monitoring Function
        while (True):
            print('Monitored')
            # Look for triggers

    def check_triggers(self):
        # Runs through each state in the State Machine
        for state in self.states:
            print("Checking Triggers for {}".format(state.name))
            state.check_transition_triggers()

    def observe_transition(self, start_state, node, transition):
        # Make Call to Run Transition
        destination_state = transition.destination
        start_state.remove_node(node)
        destination_state.add_node(node)
        self.get_network_objects()
        print('Transition From {} to {}'.format(start_state.name, transition.destination.name))

    def assign_state_nodes(self):
        for dev in self.entity_dict:
            # Get and Add Devices
            dev_obj = self.entity_dict[dev]['dev_obj']
            self.add_node_to_state(dev_obj)
            # Get and Add Device Interfaces
            dev_interfaces = self.entity_dict[dev]['interfaces']
            for iface in dev_interfaces:
                self.add_node_to_state(iface)
            # Get and Add Device Users
            dev_users = self.entity_dict[dev]['users']
            for user in dev_users:
                self.add_node_to_state(user)

    def add_node_to_state(self, node):
        if not node.current_state:
            start_state = self.get_start_state()
            node.current_state = start_state
            start_state.add_node(node)
        else:
            node.current_state.add_node(node)

    #######################
    # SSH CONTROL METHODS #
    #######################

    def open_and_move(self, device_name):
        device = self.get_dev_by_name(device_name)
        if self.device_session_status['open'].__contains__(device):
            print("Session Currently Open")
        else:
            device.open_session()
            self.device_session_status['closed'].remove(device)
            self.device_session_status['open'].append(device)
            print("Session to {} is now Open.".format(device_name))

    def close_and_move(self, device_name):
        device = self.get_dev_by_name(device_name)
        if self.device_session_status['closed'].__contains__(device):
            print("Session is Currently Closed")
        else:
            device.session.close()
            self.device_session_status['open'].remove(device)
            self.device_session_status['closed'].append(device)
            print("Session to {} is now Closed.".format(device_name))


    #############################
    # UPDATE COLLECTION METHODS #
    #############################

    def collect_and_compare(self):
        # 1.) Saves old Dictionaries
        old_dict = self.collect()  # Collects information prior to update
        # 2.) Runs Information Collector to gather more information
        # For loop that uses only open sessions to gather information
        for device in self.device_session_status['open']:
            print("Collecting Information on {}".format(device.name))
            configuration_collection(device)
            print("Configuration Collected")
        # Information Collector was used to Collect Information from every device
        #information_collector()  # Call information collector to gather update information on devices
        new_dict = self.collect()  # Collects updated information
        # 3.) Compares New Dicts to Old Dicts
        self.compare(old_dict, new_dict)
        # 4.) Puts Differences into a collection, returns collection

    def collect(self):
        collected_dict = {}
        dev_dict = get_dict('entities/junos/devices')
        for dev_name in dev_dict:
            interface_dict = get_dict('entities/junos/{}/interfaces'.format(dev_name))
            user_dict = get_dict('entities/junos/{}/users'.format(dev_name))
            tmp_dict = {dev_name: {'interfaces': interface_dict, 'users': user_dict}}
            collected_dict.update(tmp_dict)
        return collected_dict

    def compare(self, old_dict, new_dict):
        # Fix Old_dict updating devices some how. Devices Dict is updated when device is added or removed, collect can not detect old devices
        for old_device, new_device in zip(old_dict.keys(), new_dict.keys()):  # Device Level Iteration
            old_users = old_dict[old_device]['users']
            new_users = new_dict[new_device]['users']
            old_interfaces = old_dict[old_device]['interfaces']
            new_interfaces = new_dict[new_device]['interfaces']
            user_flags, added_users, removed_users = self.compare_user_dict(old_users,
                                                                            new_users)  # Calls to Compare Existing Users
            interface_flags, added_interfaces, removed_interfaces = self.compare_interface_dict(old_interfaces,
                                                                                                new_interfaces)
            self.change_list_users(user_flags, added_users, removed_users)
            self.change_list_interfaces(interface_flags, added_interfaces, removed_interfaces)

    def compare_user_dict(self, old_users, new_users):
        # Functionality: Creates a Dictionary of Consistent Users, with a list of flags for changes that had been made
        # Also Returns two lists, one for new users, one for removed users
        old_keys, new_keys = old_users.keys(), new_users.keys()
        # Finds Additions and Subtractions to the User Dict
        added_users = list(
            set(new_keys) - set(old_keys))  # Returns a set of users that have been added since last check
        removed_users = list(
            set(old_keys) - set(new_keys))  # Returns a set of users that have been removed since last check
        # Finds Consistent Users by Removing Added and Removed Users
        consistent_keys = list((set(new_keys) | set(old_keys)) - (set(added_users) | set(removed_users)))
        consistent_old_users = {key: old_users[key] for key in old_users if key in consistent_keys}
        consistent_new_users = {key: new_users[key] for key in new_users if key in consistent_keys}
        # Compares Each Value of Consistent Users for Modifications of Properties
        flag_dict = {}
        for (old_user, old_dict), (new_user, new_dict) in zip(consistent_old_users.items(),
                                                              consistent_new_users.items()):
            changed_full_name, changed_id, changed_class = False, False, False  # Each Attribute is given a boolean value, if changed, value becomes true
            if old_dict['full_name'] != new_dict['full_name']:
                changed_full_name = True
            if old_dict['id'] != new_dict['id']:
                changed_id = True
            if old_dict['class'] != new_dict['class']:
                changed_class = True
            if changed_full_name or changed_id or changed_class:
                flag_dict.update({new_user: [changed_full_name, changed_id, changed_class]})
        return flag_dict, added_users, removed_users

    def compare_interface_dict(self, old_interfaces, new_interfaces):  # For better doc, compare_user_dict
        # Gets keys of dictionaries
        old_keys, new_keys = old_interfaces.keys(), new_interfaces.keys()
        # Compares key list and gets interfaces added and removed interfaces
        added_interfaces = list(set(new_keys) - set(old_keys))
        removed_interfaces = list(set(old_keys) - set(new_keys))
        # Finds Consistent Interfaces
        consistent_keys = list((set(new_keys) | set(old_keys)) - (set(added_interfaces) | set(removed_interfaces)))
        consistent_old_interfaces = {key: old_interfaces[key] for key in old_interfaces if key in consistent_keys}
        consistent_new_interfaces = {key: new_interfaces[key] for key in new_interfaces if key in consistent_keys}
        # Compare Each Value of Consistent Interfaces for Modifications of Properties
        flag_dict = {}
        for (old_interface, old_dict), (new_interface, new_dict) in zip(consistent_old_interfaces.items(),
                                                                        consistent_new_interfaces.items()):
            changed_admin_status, changed_oper_status, changed_description = False, False, False
            if old_dict['admin-status'] != new_dict['admin-status']:
                changed_admin_status = True
            if old_dict['oper-status'] != new_dict['oper-status']:
                changed_oper_status = True
            if old_dict['description'] != new_dict['description']:
                changed_description = True
            if changed_admin_status or changed_oper_status or changed_description:
                flag_dict.update({new_interface: [changed_admin_status, changed_oper_status, changed_description]})
        return flag_dict, added_interfaces, removed_interfaces

    def change_list_users(self, user_flags, added_users, removed_users):
        for user in added_users:
            alert = "ALERT - {} is a NEW USER".format(user)
            print("ALERT - {} is a NEW USER".format(user))
            self.changes.append(alert)
        for user in removed_users:
            alert = "ALERT - {} has been REMOVED".format(user)
            print("ALERT - {} has been REMOVED".format(user))
            self.changes.append(alert)
        for user in user_flags:
            changed_name, changed_id, changed_class = user_flags[user][0], user_flags[user][1], user_flags[user][2]
            if changed_name:
                alert = "ALERT - {}'s full-name has been changed.".format(user)
                print("ALERT - {}'s full-name has been changed.".format(user))
                self.changes.append(alert)
            if changed_id:
                alert = "ALERT - {}'s id has been changed.".format(user)
                print("ALERT - {}'s id has been changed.".format(user))
                self.changes.append(alert)
            if changed_class:
                alert = "ALERT - {}'s class has been changed.".format(user)
                print("ALERT - {}'s class has been changed.".format(user))
                self.changes.append(alert)

    def change_list_interfaces(self, interface_flags, added_interfaces, removed_interfaces):
        for iface in added_interfaces:
            alert = "ALERt - {} is a NEW INTERFACE".format(iface)
            self.changes.append(alert)
        for iface in removed_interfaces:
            alert = "ALERt - {} is a REMOVED INTERFACE".format(iface)
            self.changes.append(alert)
        for iface in interface_flags:
            changed_admin, changed_oper, changed_desc = interface_flags[iface][0], interface_flags[iface][1], \
                                                        interface_flags[iface][2]
            if changed_admin:
                alert = "ALERT - {}'s admin-status has changed.".format(iface)
                self.changes.append(alert)
            if changed_oper:
                alert = "ALERT - {}'s oper-status has changed.".format(iface)
                self.changes.append(alert)
            if changed_desc:
                alert = "ALERT - {}'s description has changed.".format(iface)
                self.changes.append(alert)


