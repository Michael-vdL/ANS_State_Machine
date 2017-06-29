# Main Window of Application
# Provides Access to:
# 1.) Workshop Tool
# 2.) Observer Start and Stop
# 3.) Testing Tools
# foo_helper() methods are just drivers for different options

from workshop.SM_WorkShop import *
from workshop.SM_Builder import *
from objects.SM_Observer import *

def hub_helper():
    print("Welcome to the ANS - Network State Machine: ")
    print("What would you like to do: ")
    print("Option 1.) Start up an Observer")
    print("Option 2.) Enter Workshop Editor")
    print("Option 3.) Open the Testing Menu")
    print("Option 0.) Leave Program")
    choice = input("Please Select an Option(Enter Number): ")
    if choice == '0':
        print("Thank you for using Network State Machine")
        return
    elif choice == '1':
        observer_helper()
        return hub_helper()
    elif choice == '2':
        workshop_helper()
        return hub_helper()
    elif choice == '3':
        test_helper()
        return hub_helper()
    else:
        print("Sorry that is not an Option, please try again.")
        return hub_helper()

def observer_helper():
    state_dict = get_state_dict()
    trans_dict = get_trans_dict()
    obsv = sm_builder(state_dict, trans_dict)
    print("Observer Built: {}".format(obsv.name))
    return

def workshop_helper():
    print("...Entering Workshop...")
    workshop_intro()
    return

def test_helper():
    return

if __name__ == '__main__':
    hub_helper()
