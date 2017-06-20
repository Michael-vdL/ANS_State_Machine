#!/usr/bin/python

from Get_Fished import *
from SM_Abstracts import *
from SM_FIle_Unloader import *
from SM_File_Loader import *
from SM_Maker import *
from SM_Observer import *
from SM_Tester import *
from mininet.net import Mininet


if __name__ == '__main__':
    print("#################################")
    print("Welcome Driver Testing Environment - ")
    print("#################################")
    driving = True
    state_dict = {}
    trans_dict = {}
    update_dict = {}
    while(driving):
        print("0.) Show Instructions for First time use")
        print("1.) Making States.")
        print("2.) Making Transitions.")
        print("3.) Writing Files")
        print("4.) Reading Files")
        print("5.) Print State Location of Each Node")
        print("6.) Test Transition")
        print("7.) Test Fishing Example")
        choice = raw_input("Enter the option you would like to test: ")
        if choice == '1':
            print("Launching SM Maker - Making States")
            state_dict = get_state_input()
        elif choice == '2':
            print("Launching SM Maker - Making Transitions")
            trans_dict = get_transition_input()
        elif choice == '3':
            print("Writing Files")
            on_write(state_dict, trans_dict, update_dict)
        elif choice == '4':
            print("Loading Files")
            obsv = Observer('test_obs',on_load('states.txt', 'transitions.txt', 'update.txt'), run_net())
        elif choice == '5':
            print("Checking Node Location")
            obsv.state_check()
        elif choice == '6':
            print("Running Test Transition")
            obsv.test_transition()
            obsv.run_transitions()
        elif choice == '7':
            print("Testing Fishing Example")
            compromised_host = initiate_fishing(obsv.net)
            obsv.update_log.append(compromised_host)
            obsv.listening()
        elif choice == '8':
            print("Instruction Set - ")
            print("Currently this program allows you to write the name of the state, give it transition permissions")
            print("write transitions, save them to a file, load the file and a mininet to test a few simple use cases.")
            print("Because of the lack of modular functionality for transitions(Next thing to work on) I would recommend just using option 4.")
            print("First time Users: Option 4, to load from files and start a mininet. Then Option 5, to see states. Then option 6, to move new nodes into new state. Then option 7 to see the transition from new to unhealthy")
            print("For those looking for risks in life: Option 1, enter a state name, one of your states must be named 'start'. The transition perm you provide correlates to the swap_code of the transitions you make in option 2.")
            print("The functional transitions at the moment are only to_new, and to_unhealthy. You can add more by mimicing the mark_new functions in SM_Abstracts")
            print("It works as intended but could be much prettier and much more modular")
        else:
            print("Done Testing Driver")
            obsv.net_stop()
            driving = False
        print("#################################")
