# Proto


def workshop_transition_editor(current_trans_dict):
    trans_dict = {}
    print("#################################")
    print("Welcome to Transition Editor")
    print("#################################")
    choice = input("What would you like to do? (New, Cancel, Edit): ")
    choice = choice.lower()

    if choice == 'cancel':
        print("...Leaving Transition Editor...")
        trans_dict.update(current_trans_dict)
        return trans_dict
    elif choice == 'new':
        # Section for making New Transition
        # Functionality:
        # 1.)Input a Trans Name --> Checks to make sure no state like that already exits
        # 2.)Input a Trans To --> Assigns Transition Destination
        # 3.)Input a Tran Func --> *temp_idea* John Suggested a Middle Man State--> Could be how we implement that

        # Calls Functions, Updates Dict, Recalls Transition Editor with New Dictionary
        trans_dict.update(new_transition())
        trans_dict.update(current_trans_dict)
        return workshop_transition_editor(trans_dict)
    elif choice == 'edit':
