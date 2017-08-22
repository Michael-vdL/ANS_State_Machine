# File Holds Triggers

def trigger_handler(trigger, node):
    TRIGGERS = {'node_is_new_user': node_is_new_user,
                'node_is_new_interface': node_is_new_user,
                'node_is_new_device': node_is_new_device,
                }

    return TRIGGERS[trigger](node)


def node_is_new_user(node):
    if node.new and node.node_type == 'User':
        return True
    else:
        return False


def node_is_new_interface(node):
    if node.new and node.node_type == 'Interface':
        return True
    else:
        return False


def node_is_new_device(node):
    if node.new and node.node_type == 'Device':
        return True
    else:
        return False
