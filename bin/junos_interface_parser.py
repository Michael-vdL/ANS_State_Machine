import xml.etree.ElementTree
import json


# XPath Test
def parse_interface(file_path):
    interface_dict = {}
    tree = xml.etree.ElementTree.parse('{}/interfaces.xml'.format(file_path))
    root = tree.getroot()
    physical_interfaces = root.findall("*/")
    for interface in physical_interfaces:
        name, dict = parse_physical_interface(interface)
        tmp_dict = {name: dict}
        interface_dict.update(tmp_dict)
    with open('{}/interfaces.json'.format(file_path), 'w') as resource_file:
        json.dump(interface_dict, resource_file)


def parse_physical_interface(interface):
    name = interface.find('name').text.strip()
    admin_status = interface.find('admin-status').text.strip()
    oper_status = interface.find('oper-status').text.strip()
    if interface.find('description') is not None:
        description = interface.find('description').text.strip()
    else:
        description = 'None'
    logical_interfaces = interface.findall("logical-interface")
    logical_interface_dict = {}
    for log_interface in logical_interfaces:
        dict_name, dict = parse_logical_interface(log_interface)
        tmp_dict = {dict_name: dict}
        logical_interface_dict.update(tmp_dict)
    return name, {'admin-status': admin_status, 'oper-status': oper_status, 'description': description,
                  'logical_interfaces': logical_interface_dict}


def parse_logical_interface(interface):
    name = interface.find('name').text.strip()
    admin_status = interface.find('admin-status').text.strip()
    oper_status = interface.find('oper-status').text.strip()
    if interface.find('filter-information') is not None:
        filter_information = interface.find('filter-information').text.strip()
    else:
        filter_information = 'None'
    # Get Address Family Information
    address_families = interface.findall('address-family')
    address_family_dict = {}
    for family in address_families:
        dict_name, dict = parse_address_family(family)
        tmp_dict = {dict_name: dict}
        address_family_dict.update(tmp_dict)
    return name, {'admin_status': admin_status, 'oper_status': oper_status, 'filter_information': filter_information,
                  'address_families': address_family_dict}


def parse_address_family(family):
    name = family.find('address-family-name').text.strip()
    interface_addresses = family.findall('interface-address')
    interface_address_list = []
    for address in interface_addresses:
        interface_address_list.append(parse_interface_address(address))
    return name, interface_address_list


def parse_interface_address(address):
    if address.find('ifa-local') is not None:
        local = address.find('ifa-local').text.strip()
    else:
        local = 'None'
    if address.find('ifa-destination') is not None:
        destination = address.find('ifa-destination').text.strip()
    else:
        destination = 'None'
    return {'local': local, 'destination': destination}


if __name__ == '__main__':
    parse_interface()
