from gui.GUI_Application_Hub import *

import os
import sys
import paramiko
import urllib.request


# !/usr/bin/python

class Juniper_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.device_dict = {}
        self.initUI()

    def initUI(self):
        # Functionality:
        # Create List of Juniper Devices that can be accessed (File based for now, maybe there is some other way to track this?)
        # Create a CLI Window to those juniper devices
        ################################################
        top_layout = QHBoxLayout()
        # 1.) Create List
        self.initDevice(top_layout)

        #Layout and Geometry
        self.setLayout(top_layout)
        self.setWindowTitle("Juniper Control")

    def initDevice(self, layout):
        # Layout Features
        device_grpbx = QGroupBox("Device List")
        device_layout = QVBoxLayout()
        device_button_layout = QHBoxLayout()
        # List
        self.device_list = QListWidget()
        # Add Items to Device List (Do from Json File with HostName, Ip, username, password) For now just temp one device for testing
        temp_device_item = QListWidgetItem('vSRX-1 - 192.168.0.1')
        self.device_list.addItem(temp_device_item)

        #############Buttons###################
        # Create Buttons
        btn_add_device = QPushButton("Add Device")
        btn_remove_device = QPushButton("Remove Device")
        # Resize buttons
        btn_add_device.resize(btn_add_device.sizeHint())
        btn_remove_device.resize(btn_remove_device.sizeHint())
        # Connect Buttons
        # Add Buttons
        device_button_layout.addWidget(btn_add_device)
        device_button_layout.addWidget(btn_remove_device)

        # Add List and Button layout
        device_layout.addWidget(self.device_list)
        device_layout.addLayout(device_button_layout)

        device_grpbx.setLayout(device_layout)
        layout.addWidget(device_grpbx, 1)
        layout.addWidget(Interactive_Junos_GUI('vSRX-1', '192.168.0.1', 'root', 'Tester123'), 2)


class Interactive_Junos_GUI(QWidget):
    def __init__(self, name, ip, username, password):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        # Layout Design:
        # 1.top_layout -> Holds a grp_bx for CLI and CLI Interaction

        top_layout = QVBoxLayout()
        cli_list_grp_box = QGroupBox("{} CLI".format(self.name))
        cli_list_layout = QVBoxLayout()  # Holds ListWidget and List btn layout
        cli_list_btn_layout = QHBoxLayout()  # Has Line Edit for entering commands, has an enter button to enter commands

        # Widgets for CLI
        cli_list = QListWidget()
        cli_le = QLineEdit()
        cli_enter_btn = QPushButton()
        cli_list_btn_layout.addWidget(cli_le, 2)
        cli_list_btn_layout.addWidget(cli_enter_btn)
        cli_list_layout.addWidget(cli_list)
        cli_list_layout.addLayout(cli_list_btn_layout)
        cli_list_grp_box.setLayout(cli_list_layout)

        # Widgets for CLI Control
        cli_control_grp_box = QGroupBox("CLI Controls")  # Holds Launch and Close buttons
        cli_control_layout = QHBoxLayout()
        # Create Buttons
        btn_cli_launch = QPushButton('Launch CLI')
        btn_cli_close = QPushButton('Close CLI')
        # Resize Buttons
        btn_cli_launch.resize(btn_cli_launch.sizeHint())
        btn_cli_close.resize(btn_cli_close.sizeHint())
        # Connect Buttons

        # Add Buttons
        cli_control_layout.addWidget(btn_cli_launch)
        cli_control_layout.addWidget(btn_cli_close)
        cli_control_grp_box.setLayout(cli_control_layout)

        # Add Grp Boxes to Top layout
        top_layout.addWidget(cli_list_grp_box)
        top_layout.addWidget(cli_control_grp_box)
        # Set Layout
        self.setLayout(top_layout)
