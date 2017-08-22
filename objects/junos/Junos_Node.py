from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from objects.SM_Node import *


#############
# Device
#############

class Junos_Device(Node):
    def __init__(self, host_name, ip, username, password):
        Node.__init__(self, name=host_name, parent=None, node_type='Device')
        self.ip = ip
        self.username = username
        self.password = password
        self.session = self.get_ssh()

    def get_ssh(self):
        session = Device(self.ip, host=self.name, user=self.username, passwd=self.password)
        return session

    def open_session(self):
        print("Device Is Opening Session")
        try:
            self.session.open()
            print(self.session.facts)
        except ConnectError as err:
            print("Cannot connect to device: {}".format(err))
        except Exception as err:
            print(err)

    def close_session(self):
        self.session.close()

    def get_file_path(self):
        path = 'resources/entities/junos/{}'.format(self.name)
        return path


##############
# Interface
##############
class Junos_Interface(Node):
    def __init__(self, device, name, type, admin_status, oper_status, description, filter_info, address_families):
        Node.__init__(self, name=name, parent=device, node_type='Interface')
        self.iftype = type
        self.admin_status = admin_status
        self.oper_status = oper_status
        self.description = description
        if self.iftype == 'physical':
            self.filter_info = None
            self.address_families = None
        elif self.iftype == 'logical':
            self.filter_info = filter_info
            self.address_families = address_families


##############
# User
##############
class Junos_User(Node):
    def __init__(self, device, name, full_name, id, class_level):
        Node.__init__(self, name=name, parent=device, node_type='User')
        self.full_name = full_name
        self.id = id
        self.class_level = class_level
