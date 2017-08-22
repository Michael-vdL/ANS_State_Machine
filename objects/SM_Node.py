#!/usr/bin/python

class Node(object):
    def __init__(self, name, parent, node_type):
        self.name = name
        self.parent = parent
        self.node_type = node_type
        self.health_status = True  # if true, healthy, if false, unhealthy
        self.current_state = None
        self.new = True
