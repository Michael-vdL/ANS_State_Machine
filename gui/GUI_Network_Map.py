from gui.GUI_Application_Hub import *

import os
import sys
import paramiko
import urllib.request


# !/usr/bin/python

class Network_Map_GUI(QWidget):
    def __init__(self):
        super().__init__()
        # Connect/Enable SSH to ODL Host
        self.odl_ssh = paramiko.SSHClient()
        self.odl_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.odl_ssh.connect('172.31.8.19', port=22, username='mininet', password='mininet')
        #self.initODL()
        self.initUI()

    def initODL(self):
        print("Initializing ODL (This May Take a Minute)...")
        transport = self.odl_ssh.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()

        session.exec_command('./distribution-karaf-0.6.0-Carbon/bin/karaf\n')

    def initUI(self):
        # Layout
        top_layout = QVBoxLayout()
        # Buttons
        btn_launch_odl = QPushButton('Launch OpenDaylight', self)

        # Buttons Resize
        btn_launch_odl.resize(btn_launch_odl.sizeHint())

        # Buttons Connect
        # btn_launch_odl.clicked.connect(self.click_launch_odl)

        # Add Buttons to Layout
        top_layout.addWidget(btn_launch_odl)

        # Set Layout and Title
        self.setLayout(top_layout)
        self.setWindowTitle("Network Map")
