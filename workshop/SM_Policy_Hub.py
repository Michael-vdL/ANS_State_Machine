# Current Plans
# Main Purpose: This will be the main editing page for Policies, Realms, Rules, Policy Groups, and also *thinking* about some sort of class of service management
# Functionalities (A lot of these are pulled from the ideas behind CISCO realm fundementals)
# 1.) Realm Editor - Allows the User to Edit Realms, which can be assigned to states/transitions
# i.) Name
# ii.) Description
# iii.) Type - Policy or CoS (Idea here is that a State can have both a Policy and a CoS realm assigned)
# iv.) Transitions - Idea here is that we could move transition control away from the state, and give it to realms because where you can move has more to do with what policies are being enforced than where you are
# v.) Members - Allows the seperation of state members into seperate Policy and CoS classes, even if in the same state
# Example: You have two printers, one of them is the bosses printer, one of them is the companies printer
# You dont want to have the boss to wait, but you want them to have the same policy enforcement because they are both printers
# So you give the Policy realm all the members, and give the


# Other Idea for CoS and Policy:
# All Realms are Policy Realms, Observer has seperate CoS groups that it manages
# Each Node in the Network has a State, and a CoS group, rather than only a state that has Policy and CoS
