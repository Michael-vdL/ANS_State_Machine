# Funcationality:
# Goes through each Device entry in resources/entities/junos/devices.json
# For Each Device, run commands to get operational data (maybe even a file stream)
# Builds a directory for that device (e.g. resources/entities/junos/<device-hostname>
# Directory will contain ->
# facts.json -> stores basic information about device
# users.json -> stores user data
# interfaces.json -> stores interfaces
# routes.json -> stores route data
# policy.json -> stores policy data?

# Current Approach ->
# 1.) Call RPC Commands
# 2.) Save output to txt file
# 3.) Send it to parser
# 4.) Save it to <entity-name>.json file
# (It will then be used for building actual entities, comparison checks for changed data, autonomous configuration changes)

import json
import os
import pathlib
import errno
from lxml import etree
import xmltodict
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from bin.junos_interface_parser import parse_interface
from resources.JunosTables.ConfigTables import UserTable, PolicyTable, PolicyRuleTable, ZoneTable


# Reads the devices.json, creates SSH connection, creates open device list, builds directories
def information_collector():
    # Read Device file
    with open('resources/entities/junos/devices.json', 'r') as resource_file:
        device_dict = json.load(resource_file)
    # Parse Device Connection Information:
    for dev_hostname in device_dict:
        dev_ip = device_dict[dev_hostname]['ip']
        dev_user = device_dict[dev_hostname]['username']
        dev_passwd = device_dict[dev_hostname]['password']
        print(dev_hostname, dev_ip, dev_user, dev_passwd)
        # Make Directory for Device:
        dev_path = make_directory(dev_hostname)
        # Open Session to Device:
        session = make_session(dev_hostname, dev_ip, dev_user, dev_passwd)
        # Send Session to Parsers:
        collect_interfaces(dev_path, session)
        collect_users(dev_path, session)
        # parse_routes(dev_path, session) #May not be used
        collect_policy(dev_path, session)
        collect_zones(dev_path, session)
        # Close Connection
        session.close()


# Takes in a dev_hostname, makes directory for device
def make_directory(dev_hostname):
    file_name = 'resources/entities/junos/{}'.format(dev_hostname)
    pathlib.Path(file_name).mkdir(parents=True, exist_ok=True)
    return file_name


# Takes in a device, returns an open session to add to session list
def make_session(dev_hostname, dev_ip, dev_user, dev_passwd):
    session = Device(dev_ip, host=dev_hostname, user=dev_user, passwd=dev_passwd)
    try:
        session.open()
        print(session.facts)
    except ConnectError as err:
        print("Cannot connect to device: {}".format(err))
    except Exception as err:
        print(err)
    return session


# Sends device, show interfaces terse, saves to text file, parses file
# 1.) Parser Takes in Path for device directory and an opensession with device
# 2.) Sends CLI command to get xml output of response (Swap to RPC command when finalized, also, if Junos {['format':'json']} works, we could skip parsing and just save that as JSON)
# 3.) Parses xml into JSON objects
def collect_interfaces(dev_path, session):
    rsp = session.cli('show interfaces terse', format='xml', warning=False)
    element_tree = rsp.getroottree()
    element_tree.write('{}/interfaces.xml'.format(dev_path))
    parse_interface(dev_path)


def collect_users(dev_path, session):
    users = UserTable(session).get()  # Gets users list from UserTable on device
    user_dict = {}  # Starts the Dict for JSON
    for user in users:  # Iterates over users
        tmp_dict = {user.username: {'full_name': user.userfullname, 'id': user.userid,
                                    'class': user.userclass}}  # Stores Users in tmp_dict
        user_dict.update(tmp_dict)  # Updates whole dict with entry
    with open('{}/users.json'.format(dev_path), 'w') as resource_file:  # Dumps to correct JSON File
        json.dump(user_dict, resource_file)


# Not Calling Because It may not be useful
def parse_routes(dev_path, session):
    rsp = session.cli('show route', format='xml', warning=False)
    element_tree = rsp.getroottree()
    element_tree.write('{}/routes.xml'.format(dev_path))


def collect_policy(dev_path, session):
    policies = PolicyTable(session).get()
    policy_dict = {}
    for context in policies:
        policy_list = [context.from_zone_name, context.to_zone_name]
        policy_rules = PolicyRuleTable(session).get(policy=policy_list)
        for policy_name in policy_rules:
            policy = str(policy_name).split(':')[1]
            tmp_dict = {policy: {'from': policy_list[0], 'to': policy_list[1], 'source': policy_name.match_src,
                                 'dest': policy_name.match_dst, 'app': policy_name.match_app}}
            policy_dict.update(tmp_dict)
    with open('{}/policy.json'.format(dev_path), 'w') as resource_file:
        json.dump(policy_dict, resource_file)


def collect_zones(dev_path, session):
    zones = ZoneTable(session).get()
    zone_dict = {}
    for zone in zones:
        tmp_dict = {
            zone.name: {'address_book': zone.book, 'interfaces': zone.interfaces, 'in_services': zone.inboundservices,
                        'in_protocols': zone.inboundprotocols}}
        zone_dict.update(tmp_dict)
    with open('{}/zones.json'.format(dev_path), 'w') as resource_file:
        json.dump(zone_dict, resource_file)
