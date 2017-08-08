from gui.GUI_Application_Hub import *

import os
import sys
import paramiko
import urllib.request
# Juniper Imports
import yaml
from jnpr.junos import Device, Console
from jnpr.junos.factory import loadyaml, to_json
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.exception import ConnectError

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
        self.device_gui = Device_List_Junos_GUI()
        # 2.) Create CLI
        self.cli_gui = Interactive_Junos_GUI(self.device_gui)
        # 3.) Add Widgets to Top layout
        top_layout.addWidget(self.device_gui, 1)
        top_layout.addWidget(self.cli_gui, 2)

        #Layout and Geometry
        self.setLayout(top_layout)
        self.setWindowTitle("Juniper Control")


class Device_List_Junos_GUI(QWidget):
    def __init__(self):
        super().__init__()
        # Initial Data Load
        self.device_dict = self.get_device_dict()
        # UI Generation
        self.initUI()

    def initUI(self):
        # Layout/Grpbx Creation
        top_layout = QVBoxLayout()
        device_grpbx = QGroupBox("Device List")
        device_layout = QVBoxLayout()
        device_btn_layout = QHBoxLayout()
        # List Creation + Population
        self.device_lst = QListWidget()
        for item in self.device_dict:
            name = item
            list_item = QListWidgetItem(name)
            self.device_lst.addItem(list_item)
        #Button Creation
        btn_add_device = QPushButton("Add Device")
        btn_remove_device = QPushButton("Remove Device")
        #Button Resize
        btn_add_device.resize(btn_add_device.sizeHint())
        btn_remove_device.resize(btn_remove_device.sizeHint())
        # Button Connection
        btn_add_device.clicked.connect(self.click_add_device)
        btn_remove_device.clicked.connect(self.click_remove_device)
        # Widgets to Layout/Layout Creation
        device_btn_layout.addWidget(btn_add_device)
        device_btn_layout.addWidget(btn_remove_device)
        device_layout.addWidget(self.device_lst)
        device_layout.addLayout(device_btn_layout)
        device_grpbx.setLayout(device_layout)
        top_layout.addWidget(device_grpbx)
        self.setLayout(top_layout)

    def get_device_dict(self):
        import json
        with open('resources/entities/junos/devices.json') as resource_file:
            dict = json.load(resource_file)
        return dict

    def save_device_dict(self):
        import json
        with open('resources/entities/junos/devices.json', 'w') as resource_file:
            json.dump(self.device_dict, resource_file)

    # Button Click Methods
    def click_add_device(self):
        print('add device clicked')
        # Fuctionality: Open Dialog box for input, save input to dictionary, save dict to device file
        # 1.) Make Instance of Adding Widget and get Input
        self.add_device_window = Adding_Junos_Device_GUI()
        self.add_device_window.exec_()
        new_item = self.add_device_window.new_item
        self.add_device_window = None
        # 2.) Save Data from Adding Widget
        # 3.) Save to File
        # 4.) Add Item to Device List
        if new_item:
            self.device_dict.update(new_item)
            self.save_device_dict()
            for key in new_item:
                name = key
                list_item = QListWidgetItem(name)
                self.device_lst.addItem(list_item)

    def click_remove_device(self):
        # Fuctionality: Remove item from device list, remove item from dict, save dict
        #####################
        # 1.) Remove Item from List
        selected_item = self.device_lst.takeItem(self.device_lst.currentRow())
        # 2.) Find Item
        self.device_dict.pop(selected_item.text())
        # 3.) Save Dict
        self.save_device_dict()
        return


class Adding_Junos_Device_GUI(QDialog):
    def __init__(self):
        super().__init__()
        self.new_item = None
        self.initUI()

    def initUI(self):
        top_layout = QVBoxLayout()
        input_grpbx = QGroupBox("Enter Device Information: ")
        input_layout = QFormLayout()
        exit_options_layout = QHBoxLayout()

        ###Input_Layout Setup###
        # Form Labels
        lbl_name = QLabel("Name: ")
        lbl_ip = QLabel("IP Address: ")
        lbl_username = QLabel("Username: ")
        lbl_password = QLabel("Password: ")
        # Form Line Edits
        self.le_name = QLineEdit()
        self.le_ip = QLineEdit()
        self.le_username = QLineEdit()
        self.le_password = QLineEdit()
        self.le_password.setEchoMode(QLineEdit.Password)
        # Set Up Form Layout
        input_layout.addRow(lbl_name, self.le_name)
        input_layout.addRow(lbl_ip, self.le_ip)
        input_layout.addRow(lbl_username, self.le_username)
        input_layout.addRow(lbl_password, self.le_password)
        # Adding Input Layout to Input Group Box
        input_grpbx.setLayout(input_layout)

        ###Exit_Options_Layout Setup###
        # Button Creation
        btn_enter = QPushButton("Enter")
        btn_cancel = QPushButton("Cancel")
        # Button Resize
        btn_enter.resize(btn_enter.sizeHint())
        btn_cancel.resize(btn_cancel.sizeHint())
        # Button Connects
        btn_enter.clicked.connect(self.click_enter)
        btn_cancel.clicked.connect(self.click_cancel)
        # Add Button to Layout
        exit_options_layout.addWidget(btn_enter)
        exit_options_layout.addWidget(btn_cancel)

        # Add Widgets and Layout to Top Layout
        top_layout.addWidget(input_grpbx)
        top_layout.addLayout(input_layout)
        top_layout.addLayout(exit_options_layout)
        # Set Layout and Title
        self.setLayout(top_layout)
        self.setWindowTitle("... Adding Junos Device ...")

    def click_enter(self):
        # Functionality: Take Input, Save as dict item, close
        new_name = self.le_name.text()
        new_ip = self.le_ip.text()
        new_username = self.le_username.text()
        new_password = self.le_password.text()
        self.new_item = {new_name: {'ip': new_ip, 'username': new_username, 'password': new_password}}
        self.close()

    def click_cancel(self):
        print("Cancel Clicked")
        self.close()


###############END OF DEVICE LIST#################

##############START OF INTERACTIVE GUI############
class Interactive_Junos_GUI(QWidget):
    def __init__(self, device_list_gui):
        super().__init__()
        self.device_list_gui = device_list_gui
        self.configuring = False
        self.initUI()

    def initUI(self):
        # Layout Design:
        # 1.top_layout -> Holds a grp_bx for SSH and SSH Interaction
        top_layout = QVBoxLayout()
        self.cli_list_grp_box = QGroupBox("Select a Device, Click Launch")
        cli_list_layout = QVBoxLayout()  # Holds ListWidget and List btn layout
        cli_list_btn_layout = QHBoxLayout()  # Has Line Edit for entering commands, has an enter button to enter commands

        # Widgets for CLI
        self.cli_list = QListWidget()
        self.cli_le = QLineEdit()
        cli_enter_btn = QPushButton("Enter")  # Enter Button
        cli_enter_btn.resize(cli_enter_btn.sizeHint())  # Resize Enter Button
        cli_enter_btn.clicked.connect(self.click_enter)  # Click Connect Enter Button
        cli_list_btn_layout.addWidget(self.cli_le, 2)
        cli_list_btn_layout.addWidget(cli_enter_btn, 1)
        cli_list_layout.addWidget(self.cli_list)
        cli_list_layout.addLayout(cli_list_btn_layout)
        self.cli_list_grp_box.setLayout(cli_list_layout)

        # Widgets for CLI Control
        cli_control_grp_box = QGroupBox("SSH Controls")  # Holds Launch and Close buttons
        cli_control_layout = QHBoxLayout()
        # Create Buttons
        btn_cli_launch = QPushButton('Launch SSH')
        btn_cli_close = QPushButton('Close SSH')
        # Resize Buttons
        btn_cli_launch.resize(btn_cli_launch.sizeHint())
        btn_cli_close.resize(btn_cli_close.sizeHint())
        # Connect Buttons
        btn_cli_launch.clicked.connect(self.click_launch_cli)
        btn_cli_close.clicked.connect(self.click_close_cli)
        # Add Buttons
        cli_control_layout.addWidget(btn_cli_launch)
        cli_control_layout.addWidget(btn_cli_close)
        cli_control_grp_box.setLayout(cli_control_layout)

        # Add Grp Boxes to Top layout
        top_layout.addWidget(self.cli_list_grp_box)
        top_layout.addWidget(cli_control_grp_box)
        # Set Layout
        self.setLayout(top_layout)

    ################THIS IS A PLACE HOLDER UNTIL I FIND A GOOD IMPLEMENTATION OF CALLING RPC'S - MAYBE A DROP DOWN MENU WHERE YOU SELECT A FEW TABLES VIEWS#####################################
    def click_enter(self):
        import json
        # Functionality:
        # 1.) Take LineEdit information
        # 2.) Send RPC to Device
        # 3.) Get Data Back and Display
        command = self.cli_le.text()  # Get Line Edit Information
        # Searches for RPC Command, gets correct response for entered command

        if self.device:
            if self.device.cli_to_rpc_string(command):
                stdout = self.device.cli(command, format='text', warning=False)
                ###This segment is a solution to a problem, solution is not ideal###
                # Problem: output(stdout) is an object with toString properties.
                # Juniper made some object with an explicit toString that knows how to format a string
                # but doesn't know how to interate like a normal string. I.E. segmenting by line not an option
                # Solution_1: QListWidgetItem(str(stdout)) forces explicit toString, however it is not displayed properly
                # Solution_2: Save as a temp file, then read each line of file as a QListWidget Item

                """
                #Solution_1:
                item = QListWidgetItem(str(stdout))
                self.cli_list.addItem(item)
                """
                # Solution_2: Adds itmes in a weird way, but this is as good as it gets until I build a parser...
                # Why not just build a parser? because there are over 100 rpc commands that are valid, and if I was able to build a parser for all of those.
                # I'd be a lot richer than I am.
                with open('tmp_cli.txt', 'w') as resource_file:
                    resource_file.write(stdout)
                with open('tmp_cli.txt', 'r') as resource_file:
                    lines = resource_file.readlines()
                for line in lines:
                    item = QListWidgetItem(line)
                    self.cli_list.addItem(item)
                    # elif command == 'configure':
                    #   self.configuring = True
                    # elif command == 'exit':
                    #   self.configuring = False
                    # elif command == 'commit':
                    #   self.configuring = False
                    #   self.cu.commit()
                    #   self.cu.unlock()
                    #   self.cu = None
                    # elif self.configuring:
                    #   self.cu = Config(self.device)
                    #   self.cu.lock()
                    #   self.cu.load(command, format='set')
            else:
                print("Sorry: {} is not a valid command, no RPC match was found.".format(command))
        else:
            self.cli_list.addItem(QListWidgetItem('Sorry, no Device Selected. Could Not Execute Command.'))
        self.cli_le.clear()

    def click_launch_cli(self):
        # Functionality:
        # 1.) Get Data for Currently Selected Device
        # 2.) Open Juniper Device
        ################
        self.cli_list.clear()  # Clear Screen to Avoid Clutter
        # 1.) Updates Dict, Gets Currently Selected Device, Saves information to open device
        self.device_dict = self.device_list_gui.get_device_dict()  # Updates Local Device List
        current_item = self.device_list_gui.device_lst.currentItem()  # Gets Selected Item from Device List
        dev_hostname = current_item.text()
        dev_ip = self.device_dict[dev_hostname]["ip"]
        dev_username = self.device_dict[dev_hostname]["username"]
        dev_password = self.device_dict[dev_hostname]["password"]
        # 2.) Opens Connection to Juniper Device

        # Below is the Device Option -> Used for RPC and YAML Tables
        self.device = Device(dev_ip, host=dev_hostname, user=dev_username, passwd=dev_password)  # Creates device object
        try:
            self.device.open()
            print(self.device.facts)
        except ConnectError as err:
            print("Cannot connect to device: {0}".format(err))
        except Exception as err:
            print(err)
        self.cli_list_grp_box.setTitle("{} - {}".format(dev_hostname, dev_ip))
        self.cli_list.addItem(QListWidgetItem("Connection to {} is now Open!".format(dev_hostname)))

    def click_close_cli(self):
        # Functionality:
        # 1.) Close Juniper Device
        if self.device:
            self.device.close()
            self.device = None
            self.cli_list_grp_box.setTitle("")
            self.cli_list.addItem(QListWidgetItem("Connection Closed."))
        else:
            print('No Device Open')


class Juniper_Device_Table_GUI(QWidget):
    def __init__(self, device, table):
        super().__init__()

    #def initUI(self):
