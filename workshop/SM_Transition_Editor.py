# Proto




def workshop_transition_editor(current_trans_dict, start_trans_dict):
    trans_dict = {}
    print("#################################")
    print("Welcome to Transition Editor")
    print("#################################")
    choice = input("What would you like to do? (New, Edit, Remove, List, Exit, No Save): ")
    choice = choice.lower()

    if choice == 'exit':
        # Functionality:
        # Exits State Creation and Saves Changes
        print("...Leaving Transition Editor - w/ Save...")
        trans_dict.update(current_trans_dict)
        return trans_dict

    elif choice == 'no save':
        # Functioanlity:
        # 1.) Returns start_state_dict --> Stores with each pass so changes don't get applied
        print("...Leaving Transition Editor - w/o Save...")
        return start_trans_dict

    elif choice == 'new':
        # Section for making New Transition
        # Functionality:
        # 1.)Input a Trans Name --> Checks to make sure no state like that already exits
        # 2.)Input a Trans Dest --> Assigns Transition Destination
        # 3.)Input a Trans Func --> *temp_idea* John Suggested a Middle Man State--> Could be how we implement that

        # Calls Functions, Updates Dict, Recalls Transition Editor with New Dictionary
        trans_dict.update(new_transition())
        trans_dict.update(current_trans_dict)
        return workshop_transition_editor(trans_dict, start_trans_dict)

    elif choice == 'edit':
        # Functionality:
        # 1.)Input a Transition Name --> Checks to make sure state exits --> Bonus: Asks if you would like to make a new state with that name
        # 2.)Allow Editing Name --> Checks to make sure new name doesn't already exist
        # 3.)Allow Editing Destination -->
        # 4.)Allow Editing Function

        # Calls Function, Updates Dict, Recalls State Editor With New Dictionary
        trans_dict = edit_transition(current_trans_dict, None)
        return workshop_transition_editor(trans_dict, start_trans_dict)

    elif choice == 'remove':
        # Functionality:
        # Removes Selected Transition From Dict
        trans_dict = remove_transition(current_trans_dict)
        return workshop_transition_editor(trans_dict, start_trans_dict)

    elif choice == 'list':
        # Functionality:
        # Lists all transitions
        list_transition(current_trans_dict)
        return workshop_transition_editor(current_trans_dict, start_trans_dict)

    else:
        print("Sorry, that's not an option.")
        trans_dict.update(current_trans_dict)
        return workshop_transition_editor(trans_dict, start_trans_dict)


# Function Group for Options

def new_transition():
    # 1.)Input a Transition Name
    trans_name = input("Enter Name of Transition you would like to add: ")
    # Error Check: Check if Transition Already Exists
    # 2.)Input a Transition Destination
    trans_dest = input("Enter Destination for Transition {}: ".format(trans_name))
    # 3.)Input a Transition Function
    trans_func = input("Enter a Function for Transition {}: ".format(trans_name))
    print("...Adding New Transition: {}...".format(trans_name))
    return {trans_name: {'dest': trans_dest, 'func': trans_func}}


def edit_transition(current_trans_dict, name):
    # 1.)Input a Transition name
    if not name:
        trans_name = input(
            "Please enter the name of the Transitions you would like to edit(list to view list of transitions): ")
        # Error CheckL Existance Check
        return edit_transition(current_trans_dict, trans_name)
    elif name == 'list':
        list_transition(current_trans_dict)
        return edit_transition(current_trans_dict, None)
    elif not current_trans_dict.__contains__(name):
        print("Sorry that Name Does Not Exist, Please Try Again")
        return edit_transition(current_trans_dict, None)
    else:
        trans_name = name
        trans_dict = current_trans_dict
        editing_trans = trans_dict.pop(trans_name)
        choice = input("What Property would you like to Edit(Name, Destination, Function, Done): ")
        choice = choice.lower()

        if choice == 'done':
            print("...Finished Editing Transition: {}...".format(trans_name))
            update_dict = {trans_name: editing_trans}
            trans_dict.update(update_dict)
            return trans_dict
        # 2.)Input for New Name
        elif choice == 'name':
            new = input("Enter new Name for Transition: ")
            update_dict = {new: editing_trans}
            trans_dict.update(update_dict)
            return edit_transition(trans_dict, new)
        # 3.)Input for New Destination
        elif choice == 'destination':
            new = input("Enter new Destination for Transition: ")
            editing_trans['dest'] = new
            update_dict = {trans_dict: editing_trans}
            trans_dict.update(update_dict)
            return edit_transition(trans_dict, trans_name)
        # 4.)Input for New Function
        elif choice == 'function':
            new = input("Enter new Function for Transition: ")
            editing_trans['func'] = new
            update_dict = {trans_dict: editing_trans}
            trans_dict.update(update_dict)
            return edit_transition(trans_dict, trans_name)
        else:
            print("That is not one of the options, please try again.")
            return edit_transition(current_trans_dict, trans_name)


def remove_transition(trans_dict):
    remove_trans_dict = trans_dict
    # 1.)Input Transition Name
    trans_name = input(
        "Please enter the name of the Transition you would like to remove(list to view list of transitions): ")
    # Error Check: Existence Check
    if trans_name == 'list':
        list_transition(trans_dict)
        return remove_transition(trans_dict)
    elif not trans_dict.__contains__(trans_name):
        print("Sorry, that state does not exist, please try again.")
        return remove_transition(trans_dict)
    else:
        remove_trans_dict.pop(trans_name)
        print("...Removing State: {}...".format(trans_name))
        return remove_trans_dict


def list_transition(trans_dict):
    if len(trans_dict) == 0:
        print("...No Transitions to List...")
        return
    else:
        counter = 1
        for trans_name in trans_dict:
            trans = trans_dict[trans_name]
            print("{}.) {} - Destination: {} | Function: {}".format(counter, trans_name, trans['dest'], trans['func']))
            counter += 1
        return
