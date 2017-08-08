from objects.SM_Node import *
from objects.junos.Junos_Node import Junos_Device, Junos_Interface, Junos_User


# Get Dictionary from JSON File
def get_dict(file_name):
    import json
    with open('resources/{}.json'.format(file_name)) as resource_file:
        dict = json.load(resource_file)
    return dict


####################
# Generate Devices #
####################

def gen_devices():
    dev_list = []
    dev_dict = get_dict('entities/junos/devices')
    for dev_name in dev_dict:
        ip = dev_dict[dev_name]['ip']  # Gets IP
        username = dev_dict[dev_name]['username']  # Gets Username
        password = dev_dict[dev_name]['password']  # Gets Password
        junos_dev = Junos_Device(dev_name, ip, username, password)  # Makes Junos Device
        if not junos_dev.last_state:  # Checks state_log for if there is a last device
            junos_dev.last_state = "New"  # If not, it sets state to New
        dev_list.append(junos_dev)
    return dev_list


#######################
# Generate Interfaces #
#######################

def gen_interfaces(dev):
    interface_list = []
    interface_dict = get_dict('entities/junos/{}/interfaces'.format(dev.name))
    for phy_interface in interface_dict:
        phyface_ad_stat = interface_dict[phy_interface]['admin-status']
        phyface_op_stat = interface_dict[phy_interface]['oper-status']
        phyface_desc = interface_dict[phy_interface]['description']
        phyface_obj = Junos_Interface(dev, phy_interface, 'physical', phyface_ad_stat, phyface_op_stat, phyface_desc,
                                      None, None)
        """
        Disabled to just show Physical interfaces
        for log_interface in interface_dict[phy_interface]['logical_interfaces']:
            logface = interface_dict[phy_interface]['logical_interfaces'][log_interface]
            logface_name = log_interface
            logface_ad_stat = logface['admin_status']
            logface_op_stat = logface['oper_status']
            logface_filter = logface['filter_information']
            logface_ad_fams = logface['address_families']
            logface_obj = Junos_Interface(dev, dev.name+" : "+logface_name, 'logical', logface_ad_stat, logface_op_stat, None, logface_filter, logface_ad_fams)
            if not logface_obj.last_state:
                logface_obj.last_state = "New"
            interface_list.append(logface_obj)
        """
        if not phyface_obj.last_state:
            phyface_obj.last_state = "New"
        interface_list.append(phyface_obj)
    return interface_list


##################
# Generate Users #
##################

def gen_users(dev):
    user_list = []
    user_dict = get_dict('entities/junos/{}/users'.format(dev.name))
    for user in user_dict:
        user_full_name = user_dict[user]['full_name']
        user_id = user_dict[user]['id']
        user_class = user_dict[user]['class']
        user_obj = Junos_User(dev, user, user_full_name, user_id, user_class)
        if not user_obj.last_state:
            user_obj.last_state = "New"
        user_list.append(user_obj)
    return user_list
