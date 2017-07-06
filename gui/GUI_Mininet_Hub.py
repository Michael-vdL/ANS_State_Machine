from gui.GUI_Application_Hub import *


class Mininet_Hub_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout Setup
        self.top_layout = QVBoxLayout()  # Parent of Two Layouts 1.) List Layout, 2.) Button layout
        self.list_layout = QHBoxLayout()  # Holds vbox layouts
        self.button_layout = QHBoxLayout()  # Holds all the buttons
        self.vbox_nodes = QVBoxLayout()  # Holds all the nodes in the network
        self.vbox_links = QVBoxLayout()  # Holds all the links in the network

    def initButtons(self):
        # Making buttons
        btn_add_host = QPushButton('1.) Add Host', self)
        btn_add_switch = QPushButton('2.) Add Switch', self)
        btn_add_controller = QPushButton('3.) Add Controller', self)
        btn_link_nodes = QPushButton('4.) Link Nodes', self)
        btn_remove_link = QPushButton('5.) Remove Link', self)

        # Resize Buttons
        btn_add_host.resize(btn_add_host.sizeHint())
        btn_add_switch.resize(btn_add_switch.sizeHint())
        btn_add_controller.resize(btn_add_controller.sizeHint())
        btn_link_nodes.resize(btn_link_nodes.sizeHint())
        btn_remove_link.resize(btn_remove_link.sizeHint())

        # Move Buttons

        # Click Event Connects/Calls

        # Add to Layout
        self.button_layout.addWidget(btn_add_host)
        self.button_layout.addWidget(btn_add_switch)
        self.button_layout.addWidget(btn_add_controller)
        self.button_layout.addWidget(btn_link_nodes)
        self.button_layout.addWidget(btn_remove_link)

    def initLists(self):
        # Making List Objects
        host_list = QListWidget()
        switch_list = QListWidget()
        controller_list = QListWidget()
