from gui.GUI_Application_Hub import *
from objects.SM_Observer import *

import os
import sys
import paramiko
import re
import urllib.request
import httplib2
import json


# !/usr/bin/python

class Mininet_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        # self.initODL()
        self.obsv = observer
        self.mn_widget = Interactive_CLI_GUI('Mininet', '172.31.8.21', 'mininet', 'mininet')
        self.mn_session = self.mn_widget.session
        self.initUI()

    def initUI(self):
        # Parts of the Layout
        # Maybe Change Layouts to Drop Down that when you select one of them you get that Layout
        # Top_Layout = QVBox w/ MN_Layout, ODL_Layout, NETConf_Layout
        # MN_Layout = QHBBox w/ Button Group, CLI Interactive Text
        # ODL_Layout = QHBox w/ WebPage View, CLI Interactive Text
        # NETConf_Layout = QHBox w/ Button Group

        # Layout Creation
        top_layout = QVBoxLayout()
        mn_layout = QHBoxLayout()

        # Init Sub Layous
        self.init_mn_layout(mn_layout)

        # Buttons
        btn_get_nodes_odl = QPushButton('Get Nodes', self)
        # Buttons Resize
        btn_get_nodes_odl.resize(btn_get_nodes_odl.sizeHint())
        # Buttons Connect
        btn_get_nodes_odl.clicked.connect(self.click_get_nodes)
        # Add Buttons to Layout
        top_layout.addLayout(mn_layout)
        top_layout.addWidget(btn_get_nodes_odl)

        # Set Layout and Title
        self.setLayout(top_layout)
        self.setWindowTitle("Northbound Hub")

    def init_mn_layout(self, layout):
        ##############################
        # Button Handler
        ##############################
        mn_btn_grpbx = QGroupBox("Mininet Buttons")
        mn_btn_layout = QVBoxLayout()
        # Buttons
        btn_launch_mn = QPushButton('Launch Mininet', self)
        btn_ping_mn = QPushButton('Ping Test', self)
        btn_http_example_mn = QPushButton('HTTP Example', self)
        btn_clear_mn = QPushButton('Clear Mininet', self)
        # Buttons Resize
        btn_launch_mn.resize(btn_launch_mn.sizeHint())
        btn_ping_mn.resize(btn_ping_mn.sizeHint())
        btn_http_example_mn.resize(btn_http_example_mn.sizeHint())
        btn_clear_mn.resize(btn_clear_mn.sizeHint())
        # Buttons Connect
        btn_launch_mn.clicked.connect(self.click_launch_mn)
        btn_ping_mn.clicked.connect(self.click_ping_mn)
        btn_http_example_mn.clicked.connect(self.click_http_example_mn)
        btn_clear_mn.clicked.connect(self.click_clear_mn)
        # Add Buttons to Btn_Group
        mn_btn_layout.addWidget(btn_launch_mn)
        mn_btn_layout.addWidget(btn_ping_mn)
        mn_btn_layout.addWidget(btn_http_example_mn)
        mn_btn_layout.addWidget(btn_clear_mn)
        # Add Btn_Group to Layout
        mn_btn_grpbx.setLayout(mn_btn_layout)
        layout.addWidget(mn_btn_grpbx)
        layout.addWidget(Interactive_CLI_GUI('Mininet', '172.31.8.21', 'mininet', 'mininet'))


    def click_launch_mn(self):
        print("Starting Minenet w/ ODL Controller...")
        self.mn_session.exec_command(
            'sudo -k mn --topo linear,3 --mac --controller=remote,172.31.8.19,port=6633 --switch ovs,protocols=OpenFlow13\n')
        stdin = self.mn_session.makefile('wb', -1)
        stdout = self.mn_session.makefile('rb', -1)
        stdin.write('mininet\n')
        stdin.flush()
        print("Setup Complete...")

    def click_clear_mn(self):
        #Functionality: Exits Mininet, Clears Mininet, Closes Old SSH, Opens new SSH
        print("Ending Mininet w/ ODL Controller...")
        stdin = self.mn_session.makefile('wb', -1)
        stdout = self.mn_session.makefile('rb', -1)
        # Quit MN
        stdin.write('exit\n')
        stdin.flush()
        # Clear MN
        stdin.write('sudo -k mn -c\n')
        stdin.flush()
        # Enter Sudo Password
        stdin.write('mininet\n')
        stdin.flush()
        self.mn_ssh.close()
        self.initMN()
        print('Mininet Quit and Cleared...')

    def click_ping_mn(self):
        print('Attempting Ping')
        stdin = self.mn_session.makefile('wb', -1)
        stdout = self.mn_session.makefile('rb', -1)
        stdin.write('pingall\n')
        stdin.flush()

    def click_http_example_mn(self):
        print('Starting HTTP Example')
        stdin = self.mn_session.makefile('wb', -1)
        stdout = self.mn_session.makefile('rb', -1)
        stdin.write('link s1 h1 down\n')
        stdin.flush()
        stdin.write('link s1 s2 down\n')
        stdin.flush()

    def click_get_nodes(self):
        #########################################
        # Functionality:
        # 1.) Establish Connection with Controller
        # 2.) Send GET Request for Nodes in Network
        # 3.) Return JSON of Network Nodes
        # 4.) Parse and Send Data to Observer
        ##########################################
        # 1.) Establish Connection
        h = httplib2.Http(".cache")
        h.add_credentials('admin', 'admin')
        # 2.) Send GET Request
        resp, content = h.request('http://172.31.8.19:8181/restconf/operational/opendaylight-inventory:nodes', "GET")
        # 3.) Return JSON Data/Parse
        nodes_content = json.loads(content)
        nodes_list = nodes_content['nodes']['node']
        node_obj_list = []
        for node in nodes_list:
            node_name = node['id']
            node_connections = node['node-connector']
            current_node = Node(node_name, node_connections)
            node_obj_list.append(current_node)
        # 4.) Send Data to Observer
        # Getting Start State
        for state in self.obsv.states:
            if state.type == 'start':
                start_state = state
        for node in node_obj_list:
            start_state.add_node(node)

        with open('temp.txt', 'w') as resource_file:
            json.dump(nodes_content, resource_file)

        print('Getting Network Nodes')


class Interactive_CLI_GUI(QWidget):
    def __init__(self, name, ip, username, password):
        super().__init__()
        self.first_command = True  # First Command must be a exec_command, the rest are write() + flush()
        self.name = name
        self.ip = ip
        self.un = username
        self.pw = password
        self.initCLI()
        self.initUI()

    def initCLI(self):
        # Init SSH
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, port=22, username=self.un, password=self.pw)

        # Init Transport
        transport = self.ssh.get_transport()
        self.session = transport.open_session()
        self.session.set_combine_stderr(True)
        self.session.get_pty()

    def initUI(self):
        # UI Items -> List Widget + Line Edit + Enter Button
        # Layout
        top_layout = QVBoxLayout()
        top_grp_box = QGroupBox("Mininet CLI")
        top_grp_box_layout = QVBoxLayout()
        cli_output_layout = QVBoxLayout()
        cli_input_layout = QHBoxLayout()

        # Init Layouts
        self.output_layout_handler(cli_output_layout)
        self.input_layout_handler(cli_input_layout)

        # Add to Top_Layout
        top_grp_box_layout.addLayout(cli_output_layout)
        top_grp_box_layout.addLayout(cli_input_layout)
        top_grp_box.setLayout(top_grp_box_layout)
        top_layout.addWidget(top_grp_box, 2)
        self.setLayout(top_layout)

    def output_layout_handler(self, layout):
        # UI Items -> List Widget
        self.lst_cli_output = QListWidget()
        layout.addWidget(self.lst_cli_output)

    def input_layout_handler(self, layout):
        # Line Edit and Button
        lbl_cli_input = QLabel('Input:')
        self.le_cli_input = QLineEdit()
        btn_cli_input = QPushButton('Enter', self)
        btn_cli_input.resize(btn_cli_input.sizeHint())
        btn_cli_input.clicked.connect(self.click_enter)

        # Add to CLI Input Layout: lbl->le->btn
        layout.addWidget(lbl_cli_input)
        layout.addWidget(self.le_cli_input, 3)
        layout.addWidget(btn_cli_input, 1)

    def click_enter(self):
        # Functionality:
        # Send the Input to SSH with Write() and Flush()
        # Update the List Widget w/ Output
        # Get Input
        input = self.le_cli_input.text()
        self.le_cli_input.clear()
        # Enter Input to SSH
        if self.first_command:
            self.session.exec_command(input + '\n')
            self.first_command = False
        else:
            stdin = self.session.makefile('wb', -1)
            stdin.write(input + '\n')
            stdin.flush()
        # Write Back of Input
        while True:
            # Works, But I need to add a way to always print, there are some Mininet things that Take time, and this does not allow it
            if self.session.send_ready():
                temp_output = str(self.session.recv(9999))
                output_data = self.parse_output(temp_output)
                break
            else:
                continue

        print('Enter Clicked')

    def parse_output(self, start):
        list_output = start.replace("b'", "").replace("'", '')
        re.findall(r"[\s ]+", list_output)

        list_item = QListWidgetItem(list_output)
        self.lst_cli_output.addItem((list_item))
