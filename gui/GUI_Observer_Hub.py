# Main Tab for the Observer Object



from gui.GUI_Application_Hub import *
from gui.GUI_Workshop_Hub import *
from objects.SM_State import *


def get_dict(file_name):
    import json
    with open('resources/{}.txt'.format(file_name)) as resource_file:
        dict = json.load(resource_file)
    return dict


class Observer_Hub_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 12))
        self.setToolTip('<b>Observer Hub</b> Widget')

        # Data Setup
        self.states_dict = get_dict('states')
        self.transitions_dict = get_dict('transitions')

        # Layout Setup
        self.top_layout = QVBoxLayout()
        self.states_layout = QHBoxLayout()

        # Object Initialization
        self.btn_refresh = QPushButton('Refresh', self)
        self.btn_refresh.resize(self.btn_refresh.sizeHint())
        self.btn_refresh.clicked.connect(self.click_refresh)
        self.top_layout.addWidget(self.btn_refresh)

        self.states_list = self.get_states()
        self.display_states()
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
        for state in self.states_list:
            # Initialize QT items
            vbox_state = QVBoxLayout()
            list_view = QListWidget()
            lbl_name = QLabel('State: {}'.format(state.name))
            lbl_type = QLabel('Type: {}'.format(state.type))

            state.add_node('Test This Function')
            # Add nodes to list widget
            for node in state.nodes_in_state:
                node_item = QListWidgetItem(node)
                list_view.addItem(node_item)
            # Add QT Items to layout
            vbox_state.addWidget(lbl_name)
            vbox_state.addWidget(lbl_type)
            vbox_state.addWidget(list_view)
            # Add Layouts to states_layout
            self.states_layout.addLayout(vbox_state)

    def click_refresh(self):
        print("This isn't working, going to fix this next")
