# Stores Junos Device API Functions that States are provided access to.

import json
from resources.JunosTables.ConfigTables import PolicyTable, PolicyRuleTable
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from objects.SM_Node import *
from objects.junos.Junos_Node import *

# Sample API
""""
def foo(<GET,SET>, <ENTER, LEAVE>):
    <
    DO SOME CODE HERE
    >
    gets return dicts, sets return
"""


# dev for Device Session
# req for API Request

def api_handler(node, req):
    if req == 'get_policy' and node.node_type == 'Device':
        interface_name, device, session, dev_path = get_device(node)
        tmp_dict = get_policy(session, dev_path)
        with open('{}/policy.json'.format(dev_path), 'w') as resource_file:
            json.dump(tmp_dict, resource_file)
    elif req == 'check_health' and node.node_type == 'Device':
        interface_name, device, session, dev_path = get_device(node)
        health_status = check_health(session, dev_path)
        node.health_status = health_status


def get_device(node):
    if node.parent:
        interface_name = node.name.strip().split(':')[1]
        device = node.parent
        session = device.get_ssh()
    else:
        interface_name = "Device - Not Interface"
        device = node
        session = device.get_ssh()
    dev_name = node.name.strip().split(':')[0]
    dev_path = 'resources/entities/junos/{}'.format(dev_name)
    dev_path = dev_path.strip()
    print('Session - Connected')
    return interface_name, device, session, dev_path


def get_policy(session, dev_path):
    print("Getting Policy for {}".format(dev_path))
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
    session.close()
    return policy_dict


def check_health(session, dev_path):
    print("Checking Health of {}".format(dev_path))
    health = get_policy(session, dev_path)
    if len(health.keys()) == 0:
        print('{} is Unhealthy'.format(dev_path))
        return False
    else:
        print('{} is Healthy'.format(dev_path))
        return True


def disable_interface(node):
    if not node.parent:
        print("not an interface")
    else:
        print("Disabling Interface - {}".format(node.name))
        interface_name, device, session, dev_path = get_device(node)
        with Config(session, mode='private') as cu:
            cu.load('set interfaces {} disable'.format(interface_name))
            cu.pdiff()
            cu.commit()


def enable_interface(node):
    if not node.parent:
        print("not an interface")
    else:
        print("Enabling Interface - {}".format(node.name))
        interface_name, device, session, dev_path = get_device(node)
        with Config(session, mode='private') as cu:
            cu.load('delete interfaces {} disable'.format(interface_name))
            cu.pdiff()
            cu.commit()
