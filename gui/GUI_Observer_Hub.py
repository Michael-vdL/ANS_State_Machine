# Main Tab for the Observer Object

# !/usr/bin/python

from gui.GUI_Application_Hub import *
from gui.GUI_Workshop_Hub import *
from objects.SM_Observer import *

from PyQt5 import QtCore as core

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
        self.btn_layout = QGridLayout()
        self.states_layout = QHBoxLayout()

        # Object Initialization
        self.btn_collect_and_compare = QPushButton('Collect and Compare', self)
        self.btn_refresh_network_entities = QPushButton('Refresh Network Entities', self)
        self.btn_refresh_workshop_objects = QPushButton('Refresh Workshop Objects', self)
        self.btn_collect_and_compare.resize(self.btn_collect_and_compare.sizeHint())
        self.btn_refresh_network_entities.resize(self.btn_refresh_network_entities.sizeHint())
        self.btn_refresh_workshop_objects.resize(self.btn_refresh_workshop_objects.sizeHint())
        self.btn_collect_and_compare.clicked.connect(self.click_collect_and_compare)
        self.btn_refresh_network_entities.clicked.connect(self.click_refresh_network_entities)
        self.btn_refresh_workshop_objects.clicked.connect(self.click_refresh_workshop_objects)

        self.btn_layout.addWidget(self.btn_collect_and_compare)
        self.btn_layout.addWidget(self.btn_refresh_network_entities)
        self.btn_layout.addWidget(self.btn_refresh_workshop_objects)
        self.states_list = self.obsv.states
        self.display_dict = self.display_states()

        self.top_layout.addLayout(self.btn_layout, 1)
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
            temp_dict = {counter: State_Widget_GUI(state,
                                                   self.obsv)}  # makes a temporary dictionary of counter and a Widget, to hold
            display_dict.update(temp_dict)  # Adds that dictionary entry to entire dict
            counter += 1  # Increments counter
        for display in display_dict:  # Goes through each display
            self.states_layout.addWidget(display_dict[display])  # Adds the widget of each display to the layout
        return display_dict  # Returns the display dict

    def click_collect_and_compare(self):
        self.obsv.collect_and_compare()

    def click_refresh_network_entities(self):
        # Remove Current States_Layout from top_layout
        self.top_layout.removeItem(self.states_layout)

        # Goes through all the displays in the dispaly dictionary
        for display in self.display_dict:
            self.states_layout.removeWidget(self.display_dict[display])  # First Removes the widget
            self.display_dict[display].deleteLater()  # Calls for the delete on update event
            self.display_dict[display] = None  # Sets the display widget to None

        self.states_dict = get_dict('states')  # Updates the State Dictionary
        self.transitions_dict = get_dict('transitions')  # Updates the Transition Dictionary

        self.states_list = self.obsv.states  # Updates the State List
        self.display_dict = self.display_states()  # Updates the Display Dictionary

        self.top_layout.addLayout(self.states_layout, 1)  # ReAdds the Layout to the Top_Layout
        self.repaint()  # Maybe not needed but it works
        self.update()  # Maybe not needed but it works

    def click_refresh_workshop_objects(self):
        self.obsv.get_network_objects()  # Calls refresh function on network objects


class State_Widget_GUI(QWidget):
    # Functionality
    # 1.) Saves Each State as a Widget
    # 2.) Allows them to be removed
    def __init__(self, state, observer):
        self.obsv = observer
        super().__init__()

        vbox_state = QVBoxLayout()
        tree_view = QTreeWidget()
        lbl_name = QLabel('State: {}'.format(state.name))
        lbl_type = QLabel('Type: {}'.format(state.type))

        HEADERS = ("Name", "Open", "Close")
        tree_view.setColumnCount(len(HEADERS))
        tree_view.setHeaderLabels(HEADERS)

        ######IMPORTANT#######
        # Going to need a way to have users and interfaces in different states than their parent device, but show that they are of that device (have device in the state, make name grey?)

        # Gets All the Devices in the State
        devices_in_state = self.get_devices_in_state(state)
        orphans_in_state = self.get_orphan_parents(state)

        # Adds them to display:
        self.add_to_tree(tree_view, devices_in_state,
                         False)  # Sends tree view, and dict of nodes to add, false if not orphans dict
        self.add_to_tree(tree_view, orphans_in_state, True)

        # Edit Tree View
        tree_view.setColumnWidth(0, 150)
        tree_view.setColumnWidth(1, 25)
        tree_view.setColumnWidth(2, 25)

        # Add QT Items to layout
        vbox_state.addWidget(lbl_name)
        vbox_state.addWidget(lbl_type)
        vbox_state.addWidget(tree_view)
        self.setLayout(vbox_state)

    def get_devices_in_state(self, state):
        devices_in_state = {}
        for node in state.nodes_in_state:
            if node.node_type == 'Device':
                tmp_dict = {node.name: {'interfaces': [], 'users': []}}
                devices_in_state.update(tmp_dict)
        self.get_device_entities(state, devices_in_state)
        return devices_in_state

    def get_orphan_parents(self, state):
        devices_with_orphans = {}
        for node in state.orphans_in_state:
            if not devices_with_orphans.__contains__(node.parent.name):
                devices_with_orphans.update({node.parent.name: {'users': [], 'interfaces': []}})
            if node.node_type == 'User':
                devices_with_orphans[node.parent.name]['users'].append(node.name)
            if node.node_type == 'Interface':
                devices_with_orphans[node.parent.name]['interfaces'].append(node.name)
        return devices_with_orphans

    def get_device_entities(self, state, devices_in_state):
        # For Each Device, Finds list of users and interfaces also in the state
        for dev in devices_in_state:
            #For Entities In Same State As Device
            users_in_dev = []
            iface_in_dev = []
            #For Entities In Different State as Device
            for node in state.nodes_in_state:
                if node.node_type == 'User' and node.parent.name == dev:
                    users_in_dev.append(node.name)
                elif node.node_type == 'Interface' and node.parent.name == dev:
                    iface_in_dev.append(node.name)
            devices_in_state[dev]['interfaces'] = iface_in_dev
            devices_in_state[dev]['users'] = users_in_dev

    def add_to_tree(self, tree_view, devices_in_state, orphans):
        for dev in devices_in_state:
            # Branches of Tree
            if orphans:
                device = QTreeWidgetItem([dev])
            else:
                device = Device_Tree_Item(tree_view, dev, self.obsv)  # Top of Tree
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

            # Parents Not in state


class Device_Tree_Item(QTreeWidgetItem):
    def __init__(self, parent, device, observer):
        super(Device_Tree_Item, self).__init__(parent)
        self.obsv = observer
        self.dev = device
        self.initUI()

    def initUI(self):
        # Column 0, Device Name
        self.setText(0, self.dev)

        # Column 1, Device Session Up
        self.btn_session_up = QPushButton()
        self.btn_session_up.setText("+")
        self.btn_session_up.resize(self.btn_session_up.sizeHint())
        self.treeWidget().setItemWidget(self, 1, self.btn_session_up)

        # Column 2, Device Session Down
        self.btn_session_down = QPushButton()
        self.btn_session_down.setText("-")
        self.btn_session_down.resize(self.btn_session_down.sizeHint())
        self.treeWidget().setItemWidget(self, 2, self.btn_session_down)

        # Connect buttons
        self.btn_session_up.clicked.connect(self.click_session_up)
        self.btn_session_down.clicked.connect(self.click_session_down)

    def click_session_up(self):
        print("Contacting Observer")
        self.obsv.open_and_move(self.dev)

    def click_session_down(self):
        self.obsv.close_and_move(self.dev)
