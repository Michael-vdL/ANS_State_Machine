#!/usr/bin/python

import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class Custom_Topo(Topo):
    def __init__(self, n_switches, host_counts, switch_dict, **opts):
        #Initialize Topo Super
        Topo.__init__(self, **opts)

        #Constructs a list of switches based on User Input
        switch_list = []
        for s in range(n_switches):
            switch = self.addSwitch('s{}'.format(s))
            switch_list.append(switch)
        #Adds Hosts and Links them to designated switches
        s_counter = 0
        h_counter = 0
        for h_count in host_counts:
            switch = switch_list[s_counter]
            for h in range(h_count):
                host = self.addHost('h{}'.format(h_counter))
                self.addLink(host, switch)
                h_counter+=1
            s_counter+=1
        #Establish Links Between Switches
        #For Default/Full Connectivity
        if not switch_dict:
            for switch in switch_list:
                for to_switch in switch_list:
                    if(switch is not to_switch):
                        self.addLink(switch, to_switch)
                return
        #For Custom Switch Connectivity
        else:
            for key_switch in switch_dict:
                for value in switch_dict[key_switch]:
                    self.addLink(key_switch, value)



def build_topo():
    print("Beginning Topology Setup - ")
    #Asks User for number of switches in topology
    switch_count = int(input("Enter Number of Switches for this Topology: "))
    #Asks User for number of hosts on each switch, adds them in order to the list of host counts
    host_list = []
    for switch in range(switch_count):
        n_hosts = input("Enter Number of Hosts for s{}: ".format(switch))
        host_list.append(n_hosts)
    #Asks User for Custom Switch Topology
    custom_switch_links = int(input("Would you like to customize switch links(Enter 0 - Switches have full interconnectivity. Enter 1 - Custom) (For now Custom is tempremental and before it is used I am planning on implementing a catch for connection failures): "))
    if custom_switch_links == 1:
        switch_dict = {}
        for s in range(switch_count):
            ##Raw_input is required on mininet because that runs 2.x python and I am using 3.x It will look weird but will work
            connection_string = raw_input("Enter switches that s{} connects to(Separated by Comma): ".format(s))
            connection_string.strip()
            temp_key = 's{}'.format(s)
            temp_value = connection_string.split(',')
            temp_dict = {temp_key : temp_value}
            switch_dict.update(temp_dict)
    else:
        switch_dict = None
    c_topo = Custom_Topo(switch_count, host_list, switch_dict)
    return c_topo

def run_net():
    topo = build_topo()
    setLogLevel('info')
    net = Mininet(topo)
    return net
    #net.start()
    #For checking Connections:
    #print("Dumping Host Connections")
    #dumpNodeConnections(net.hosts)
    #print("Testing Network Connectivity")
    #net.pingAll()

    ##Enter Test Matterial Here


    ##


    #net.stop()
