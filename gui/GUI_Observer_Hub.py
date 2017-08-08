# Main Tab for the Observer Object

# !/usr/bin/python

from gui.GUI_Application_Hub import *
from gui.GUI_Workshop_Hub import *
from objects.SM_Observer import *


class Observer_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 12))
        self.setToolTip('<b>Observer Hub</b> Widget')

        # Layout Setup
        self.top_layout = QVBoxLayout()
        self.states_layout = QHBoxLayout()

        # Object Initialization
        self.btn_collect_and_compare = QPushButton('Collect and Compare', self)
        self.btn_refresh = QPushButton('Refresh', self)
        self.btn_collect_and_compare.resize(self.btn_collect_and_compare.sizeHint())
        self.btn_refresh.resize(self.btn_refresh.sizeHint())
        self.btn_collect_and_compare.clicked.connect(self.click_collect_and_compare)
        self.btn_refresh.clicked.connect(self.click_refresh)
        self.top_layout.addWidget(self.btn_collect_and_compare)
        self.top_layout.addWidget(self.btn_refresh)

        self.states_list = self.obsv.states
        self.display_dict = self.display_states()
        self.top_layout.addLayout(self.states_layout, 1)
        # Set Geometry and Layout
        self.setLayout(self.top_layout)
        self.setGeometry(100, 100, 720, 480)
        self.setWindowTitle('Observer Hub')

    def get_states(self):
        # Functionality:
        # 1.) Load State Objects for Display
        state_list = []
        for state_name in self.states_dict:
            current_state = self.states_dict[state_name]
            state_obj = State(state_name, current_state['type'], current_state['trans_perms'],
                              current_state['func_perms'])
            state_list.append(state_obj)
        return state_list

    def display_states(self):
        # Functionality:
        # 1.) Displays All States onto GUI
        display_dict = {}  # Holds all States that are displayed
        counter = 0  # Increments Counter
        for state in self.states_list:  # Goes through each state in the state list
            temp_dict = {
                counter: State_Widget_GUI(state)}  # makes a temporary dictionary of counter and a Widget, to hold
            display_dict.update(temp_dict)  # Adds that dictionary entry to entire dict
            counter += 1  # Increments counter
        for display in display_dict:  # Goes through each display
            self.states_layout.addWidget(display_dict[display])  # Adds the widget of each display to the layout
        return display_dict  # Returns the display dict

    def click_collect_and_compare(self):
        self.obsv.collect_and_compare()

    def click_refresh(self):
        # Remove Current States_Layout from top_layout
        self.top_layout.removeItem(self.states_layout)

        # Goes through all the displays in the dispaly dictionary
        for display in self.display_dict:
            self.states_layout.removeWidget(self.display_dict[display])  # First Removes the widget
            self.display_dict[display].deleteLater()  # Calls for the delete on update event
            self.display_dict[display] = None  # Sets the display widget to None

        self.states_dict = get_dict('states')  # Updates the State Dictionary
        self.transitions_dict = get_dict('transitions')  # Updates the Transition Dictionary

        self.obsv.get_network_objects()  # Calls refresh function on network objects

        self.states_list = self.obsv.states  # Updates the State List
        self.display_dict = self.display_states()  # Updates the Display Dictionary

        self.top_layout.addLayout(self.states_layout, 1)  # ReAdds the Layout to the Top_Layout
        self.repaint()  # Maybe not needed but it works
        self.update()  # Maybe not needed but it works

class State_Widget_GUI(QWidget):
    # Functionality
    # 1.) Saves Each State as a Widget
    # 2.) Allows them to be removed
    def __init__(self, state):
        super().__init__()

        vbox_state = QVBoxLayout()
        tree_view = QTreeWidget()
        lbl_name = QLabel('State: {}'.format(state.name))
        lbl_type = QLabel('Type: {}'.format(state.type))

        ######IMPORTANT#######
        # Going to need a way to have users and interfaces in different states than their parent device, but show that they are of that device (have device in the state, make name grey?)

        # Gets All the Devices in the State
        devices_in_state = {}
        for node in state.nodes_in_state:
            if node.node_type == 'Device':
                tmp_dict = {node.name: {'interfaces': [], 'users': []}}
                devices_in_state.update(tmp_dict)

        # For Each Device, Finds list of users and interfaces also in the state
        for dev in devices_in_state:
            users_in_dev = []
            iface_in_dev = []
            for node in state.nodes_in_state:
                if node.node_type == 'User':
                    users_in_dev.append(node.name)
                elif node.node_type == 'Interface':
                    iface_in_dev.append(node.name)
            devices_in_state[dev]['interfaces'] = iface_in_dev
            devices_in_state[dev]['users'] = users_in_dev

        # Adds them to display:

        for dev in devices_in_state:
            device = QTreeWidgetItem([dev])  # Top of Tree
            user_tab = QTreeWidgetItem(["Users: "])  # First Branch of Tree
            interface_tab = QTreeWidgetItem(["Interfaces: "])  # Same Level as User Tab
            # Make and Add Children to User_tab
            for user in devices_in_state[dev]['users']:
                user_item = QTreeWidgetItem([user])
                user_tab.addChild(user_item)
            for interface in devices_in_state[dev]['interfaces']:
                interface_item = QTreeWidgetItem([interface])
                interface_tab.addChild(interface_item)
            device.addChild(user_tab)
            device.addChild(interface_tab)
            tree_view.addTopLevelItem(device)

        # Edit Tree View
        tree_view.header().close()

        # Add QT Items to layout
        vbox_state.addWidget(lbl_name)
        vbox_state.addWidget(lbl_type)
        vbox_state.addWidget(tree_view)
        self.setLayout(vbox_state)
