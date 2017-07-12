from gui.GUI_Application_Hub import *

import os
import sys
import paramiko
import urllib.request


# !/usr/bin/python

class Mininet_Hub_GUI(QWidget):
    def __init__(self):
        super().__init__()
        # self.initODL()
        self.initMN()
        self.initUI()

    def initMN(self):
        # Connect/Enable SSH to MN Host
        self.mn_ssh = paramiko.SSHClient()
        self.mn_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.mn_ssh.connect('172.31.8.21', port=22, username='mininet', password='mininet')
        # Create Session for Mininet
        transport = self.mn_ssh.get_transport()
        self.mn_session = transport.open_session()
        self.mn_session.set_combine_stderr(True)
        self.mn_session.get_pty()

    def initUI(self):
        # Layout
        top_layout = QVBoxLayout()
        # Buttons
        btn_launch_mn = QPushButton('Launch Mininet', self)
        btn_clear_mn = QPushButton('Clear Mininet', self)
        btn_ping_mn = QPushButton('Ping Test', self)
        # Buttons Resize
        btn_launch_mn.resize(btn_launch_mn.sizeHint())
        btn_clear_mn.resize(btn_clear_mn.sizeHint())
        btn_ping_mn.resize(btn_ping_mn.sizeHint())
        # Buttons Connect
        btn_launch_mn.clicked.connect(self.click_launch_mn)
        btn_clear_mn.clicked.connect(self.click_clear_mn)
        btn_ping_mn.clicked.connect(self.click_ping_mn)
        # Add Buttons to Layout
        top_layout.addWidget(btn_launch_mn)
        top_layout.addWidget(btn_clear_mn)
        top_layout.addWidget(btn_ping_mn)
        # Set Layout and Title
        self.setLayout(top_layout)
        self.setWindowTitle("Network Map")

    def click_launch_mn(self):
        print("Starting Minenet w/ ODL Controller...")

        self.mn_session.exec_command(
            'sudo -k mn --topo linear,15 --mac --controller=remote,172.31.8.19,port=6633 --switch ovs,protocols=OpenFlow13\n')
        stdin = self.mn_session.makefile('wb', -1)
        stdout = self.mn_session.makefile('rb', -1)

        stdin.write('mininet\n')
        stdin.flush()

        print("Setup Complete...")

    def click_clear_mn(self):
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
