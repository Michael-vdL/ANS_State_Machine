from gui.GUI_Application_Hub import *
from objects.SM_Observer import *


# !/usr/bin/python

class Test_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        self.top_layout = QVBoxLayout()

        # Add Test Buttons
        btn_network_test = QPushButton('Make Network', self)
        btn_add_node_test = QPushButton('Add Node Test', self)
        btn_run_transition_test = QPushButton('Run Transition Test', self)
        btn_fishing_test = QPushButton('Fishing Test', self)

        # Resize Test Buttons
        btn_network_test.resize(btn_network_test.sizeHint())
        btn_add_node_test.resize(btn_add_node_test.sizeHint())
        btn_run_transition_test.resize(btn_run_transition_test.sizeHint())
        btn_fishing_test.resize(btn_fishing_test.sizeHint())

        # Connect Test Buttons
        btn_network_test.clicked.connect(self.click_network_test)
        btn_add_node_test.clicked.connect(self.click_add_node_test)
        btn_run_transition_test.clicked.connect(self.click_run_transition_test)
        btn_fishing_test.clicked.connect(self.click_fishing_test)

        # Add Buttons to Layout
        self.top_layout.addWidget(btn_network_test)
        self.top_layout.addWidget(btn_add_node_test)
        self.top_layout.addWidget(btn_run_transition_test)
        self.top_layout.addWidget(btn_fishing_test)

        # Geometry and Layout
        self.setLayout(self.top_layout)

    def click_network_test(self):
        self.network_window = Network_Test_GUI(self.obsv)
        self.network_window.exec_()

    def click_add_node_test(self):
        from random import randint as r
        for state in self.obsv.states:
            if state.type == 'start':
                start_state = state
        node_list = self.obsv.network.node_list
        for node in node_list:
            start_state.add_node(node)

    def click_run_transition_test(self):
        from random import randint as r
        for state in self.obsv.states:
            if len(state.nodes_in_state) > 0:
                node = state.nodes_in_state[r(0, len(state.nodes_in_state))]
                transition = self.obsv.transitions[0]
                self.obsv.run_transition(state, node, transition)
                return

    def click_fishing_test(self):
        from random import randint as r
        for state in self.obsv.states:
            if len(state.nodes_in_state) > 0 and state.name == 'Healthy':
                node = state.nodes_in_state[r(0, len(state.nodes_in_state))]
                self.fish_window = Fishing_Test_GUI(node)
                self.fish_window.exec_()
                transition = self.obsv.transitions[0]
                self.obsv.run_transition(state, node, transition)
                return


class Network_Test_GUI(QDialog):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):

        # Layouts
        top_layout = QVBoxLayout()
        input_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Input Objects
        lbl_switch_count = QLabel("Enter Number of Switches: ")
        lbl_host_count = QLabel("Enter Number of Hosts per Switch: ")
        self.le_switch_count = QLineEdit()
        self.le_host_count = QLineEdit()

        # Button Objects
        btn_enter = QPushButton("Enter", self)
        btn_cancel = QPushButton("Cancel", self)

        btn_enter.resize(btn_enter.sizeHint())
        btn_cancel.resize(btn_cancel.sizeHint())

        btn_enter.clicked.connect(self.click_enter)
        btn_cancel.clicked.connect(self.click_cancel)

        # Add to Form Layout
        input_layout.addRow(lbl_switch_count, self.le_switch_count)
        input_layout.addRow(lbl_host_count, self.le_host_count)

        # Add to Button Layout
        button_layout.addWidget(btn_enter)
        button_layout.addWidget(btn_cancel)

        # Add to Top Layout
        top_layout.addLayout(input_layout)
        top_layout.addLayout(button_layout)

        # Geometry and Layout
        self.setLayout(top_layout)
        self.setWindowTitle("Setting Up Network")

    def click_enter(self):
        # Node List Start
        node_list = []
        link_list = []
        # Get Text
        switch_count = int(self.le_switch_count.text())
        host_count = int(self.le_host_count.text())
        # Add Nodes to List
        host_counter = 0
        for s in range(switch_count):
            current_switch = Node('s{}'.format(s), 'Switch')
            node_list.append(current_switch)
            for h in range(host_count):
                host_counter += 1
                current_host = Node('h{}'.format(host_counter), 'Host')
                node_list.append(current_host)
                current_link = (current_switch, current_host)
                link_list.append(current_link)

        # Link Switches
        start_switch = node_list[0]
        for node in node_list:
            if node.type == 'Switch' and node is not start_switch:
                link_list.append((start_switch, node))

        # Set Observers Network
        network = Network(node_list, link_list)
        self.obsv.set_network(network)

        # Print links
        for link in link_list:
            print(link[0].name, link[1].name)

        self.close()

    def click_cancel(self):
        self.close()


class Fishing_Test_GUI(QDialog):
    def __init__(self, node):
        super().__init__()
        print('hit fish')
        # Layouts
        top_layout = QVBoxLayout()
        input_layout = QFormLayout()

        # Objects
        lbl_text = QLabel("We're a super trustworthy site.")
        lbl_username = QLabel("Enter Username: ")
        lbl_password = QLabel("Enter Password: ")
        le_username = QLineEdit()
        le_password = QLineEdit()
        btn_enter = QPushButton('Enter', self)
        btn_cancel = QPushButton('Cancel', self)

        btn_enter.resize(btn_enter.sizeHint())
        btn_cancel.resize(btn_cancel.sizeHint())

        btn_enter.clicked.connect(self.click_enter)
        btn_cancel.clicked.connect(self.click_cancel)

        # Adding to Layouts
        input_layout.addRow(lbl_username, le_username)
        input_layout.addRow(lbl_password, le_password)
        top_layout.addWidget(lbl_text)
        top_layout.addLayout(input_layout)
        top_layout.addWidget(btn_enter)
        top_layout.addWidget(btn_cancel)

        self.setLayout(top_layout)
        self.setWindowTitle("Hey, were Fishing {}".format(node.name))

    def click_enter(self):
        self.close()

    def click_cancel(self):
        self.close()
