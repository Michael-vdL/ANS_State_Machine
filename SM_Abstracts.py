#Class for States
#Takes in load data (state_name, trans_perm_list) --> See SM_File_Loader.py

class State(object):
    def __init__(self, state_name, state_type, trans_perm_list, function_perm_list, function_item_list):
        # Static State Variables
        self.name = state_name  # Reference Name for State
        self.type = state_type  # For assigning Start(Idea : Device Discorvery State) or End(Idea : Device Removal State)
        self.perms = trans_perm_list  # Permissions for Transitions from state. Allow transitions to be global
        self.func_perms = function_perm_list  # Permissions for Functions this state has access to
        self.func_items = function_item_list  # Possible Parameters for each Function
        # Dynamic Variables
        self.nodes_in_state = []
        self.nodes_to_swap = {}

    #node management
    def add_node(self, node):
        self.nodes_in_state.append(node)

    def remove_node(self, node):
        self.nodes_in_state.remove(node)

    #Transition Management Methods
    #adds nodes to the states swap list, and labels them for the observer to swap
    def designate_swap(self, node, swap_code):
        if self.check_valid_swap(swap_code):
            update_dict = {node : swap_code} #Creates a single entity dict to update the nodes to swap
            self.nodes_to_swap.update(update_dict)
        else:
            print("Invalid Transition: Check State Transition Permission Properties")

    #Simply check if the state is allowed to make the transition that is being requested
    #Most likely will never be hit but I figure its best to be safe than sorry
    def check_valid_swap(self, swap_code):
        for perm in self.perms:
            if perm == swap_code:
                return True
            else:
                return False

    #This is the next thing to modularize
    # Idea Layout:
    # Give User Ability to Modularize a few types of Functions to work with, from WorkShop page you can mark which ones you would like to customize
    # Order for Priority to Add:
    # 1.) Mod_Enter_Func
    # 2.) Mod_Mark_Func
    # 3.) Mod_Input_Func
    # 4.) TBD

    # enter_fucntion --> When you enter state do_x --> Sample Case: 1.)Cleanse --> Items transfered into this state are suspicious and recent data should be purged. 2.) New Device --> Items in this state are new to the system and should be examined
    def mod_enter_func(self, cmd_regex, exec_file):
        cmd_list = cmd_regex.split(',')
        cmd_type = cmd_list[0]
        cmd_input = cmd_list[1]
        cmd_output = cmd_list[2]
        exec = exec_file

        return print("Enter Function Exec'd")

    # sit_function --> If sitting in state for x_length, do_x
    def mod_sit_func(self, sit_max):

        return print("Sit Function Exec'd")

    # tunnel_function --> Tunnel Control Functionality --> Establish Secure Links, Remove Unsecure Links, ReEstablish on Leave
    def mod_tunnel_func(self, controller):

        return print("Tunnels Created from " + controller)

    # input_function --> Function for Demanding User Input for This State
    def mod_input_func(self):

        return print("User Input Taken")

    # mark_functionality --> Function for Marking certain States -->  Controls Transfers
    def mod_mark_func(self):

        return print("Marked for Transfer")

    """
    def mark_new(self):
        for node in self.nodes_in_state:
            self.designate_swap(node, 'to_new')

    def mark_unhealthy(self, node):
        self.designate_swap(node, 'to_unhealthy')
    """


#Used to make Transitions Global
#Holds a transition code, used in swap management and destination state for transition
class Transition:
    def __init__(self, trans_code, to_state):
        self.code = trans_code
        self.destination = to_state