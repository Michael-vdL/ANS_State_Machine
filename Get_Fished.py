#!/usr/bin/python

import random

from SM_Tester import *
from mininet.net import Mininet

##Takes in a net
def initiate_fishing(obsvs_net):
    #Gets a list of nodes, deletes nodes that start without h (non-host nodes, i.e. Switches and Controllers)
    node_list = obsvs_net.keys()
    host_list = []
    for node in node_list:
        for char in node:
            if char == 'h':
                host_list.append(node)

    random_fish = 'h{}'.format(random.randint(0, len(host_list)))
    #Took the liberty to have some fun writing this interaction
    print("Host Getting Fished(OH NO!): ", random_fish)
    #This is just to simulate the fishing email
    print("Hey "+random_fish+", ")
    print("We are contacting you today to inform you that your company is getting HACKED!!!!!")
    print("If you enter your information below, we would be happy to send one of our online representatives your way and fix the issue for you.")

    fish_UserName = raw_input("Please Enter your Username Here(enter no to decline this one in a lifetime offer): ")
    if fish_UserName == 'no':
        print("Good Job you passed the Fish Test")
        obsvs_net.stop()
        return None

    fish_PassWord = raw_input("Please Enter your Password Here(Don't worry, were a secure site): ")
    if fish_PassWord == 'no':
        print("Good Job you passed the Fish Test")
        obsvs_net.stop()
        return None

    #Simulates Generic Warning Message
    print("Uh oh, one of your employees was just fished, and now there is malicious data on host: ",random_fish)
    return random_fish
