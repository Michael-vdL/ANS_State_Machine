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
        self.btn_refresh = QPushButton('Refresh', self)
        self.btn_refresh.resize(self.btn_refresh.sizeHint())
        self.btn_refresh.clicked.connect(self.click_refresh)
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
        display_dict = {}
        counter = 0
        for state in self.states_list:
            temp_dict = {counter: State_Widget_GUI(state)}
            display_dict.update(temp_dict)
            counter += 1

        for display in display_dict:
            self.states_layout.addWidget(display_dict[display])

        return display_dict

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
        print("Updates Finally Work")


class State_Widget_GUI(QWidget):
    # Functionality
    # 1.) Saves Each State as a Widget
    # 2.) Allows them to be removed
    def __init__(self, state):
        super().__init__()

        vbox_state = QVBoxLayout()
        list_view = QListWidget()
        lbl_name = QLabel('State: {}'.format(state.name))
        lbl_type = QLabel('Type: {}'.format(state.type))

        # Add nodes to list widget
        for node in state.nodes_in_state:
            node_item = QListWidgetItem(node.name)
            list_view.addItem(node_item)
        # Add QT Items to layout
        vbox_state.addWidget(lbl_name)
        vbox_state.addWidget(lbl_type)
        vbox_state.addWidget(list_view)
        self.setLayout(vbox_state)
