# GUI File for SM_Workshop_Hub

# !/usr/bin/python3
import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, \
    QToolTip, QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont

from gui.GUI_Workshop_Adding_Widget import *


# BACKGROUND FUNCTIONS
def get_resources():
    from os import listdir
    resource_list = [file for file in listdir('resources')]
    return resource_list


def get_dict(file_name):
    import json
    with open('resources/{}.txt'.format(file_name)) as resource_file:
        dict = json.load(resource_file)
    return dict


def save_dict(file_name, saving_dict):
    import json
    with open('resources/{}.txt'.format(file_name), 'w') as resource_file:
        json.dump(saving_dict, resource_file)


# GUI FUNCTIONS
class Workshop_Hub_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tooltops
        QToolTip.setFont(QFont('SansSerif', 12))
        self.setToolTip('<b>WorkShop Hub</b> Widget')

        # Data Setup
        self.states_dict = get_dict('states')
        self.transitions_dict = get_dict('transitions')
        self.current_dict = None

        # Layout Setup

        # Creation of Layout
        self.top_layout = QHBoxLayout()
        self.vbox_left = QVBoxLayout()
        self.vbox_right = QVBoxLayout()
        self.hbox_action_buttons = QHBoxLayout()
        self.hbox_table_widget = QHBoxLayout()

        # Assinging Stretch
        self.vbox_left.addStretch(1)

        # Adding Widgets
        self.swap_buttons(self.vbox_left)  # Call to button method -> sends a layout to add the buttons to
        self.action_buttons(self.hbox_action_buttons)
        self.table_dict = QTableWidget()
        self.hbox_table_widget.addWidget(self.table_dict)

        # Combining Layouts
        self.vbox_right.addLayout(self.hbox_action_buttons)
        self.vbox_right.addLayout(self.hbox_table_widget)
        self.top_layout.addLayout(self.vbox_left)
        self.top_layout.addLayout(self.vbox_right)

        # Setting Geometry and Layout
        self.setLayout(self.top_layout)
        self.setGeometry(100, 100, 720, 480)
        self.setWindowTitle('Workshop Hub')

    # Method for view Dictionary as List
    # Functionality: Should be able to convert any dictionaries into viewable, and interactable lists
    def dictionary_list_widget(self, dict):
        # Getting Lists of Values
        item_list = []
        for item_name in dict:
            current_item = []
            current_item.append(item_name)
            item = dict[item_name]
            for property in item:
                item_property = item[property]
                current_item.append(item_property)
            item_list.append(current_item)

        # Getting Sizes for Table Declaration
        dict_table = QTableWidget()
        row_count = len(item_list)
        column_count = len(item_list[0])
        dict_table.setRowCount(row_count)
        dict_table.setColumnCount(column_count)

        # Adding Items to the Table
        current_row = 0
        for item in item_list:
            current_column = 0
            for property in item:
                table_item = QTableWidgetItem(str(property))
                dict_table.setItem(current_row, current_column, table_item)
                current_column += 1
            current_row += 1
        return dict_table

    # Method for Adding Buttons and Following Methods for Click Events
    def swap_buttons(self, layout):
        # Instatiate Buttons
        btn_states = QPushButton('1.) States', self)
        btn_transitions = QPushButton('2.) Transitions', self)
        btn_roles = QPushButton('3.) Roles', self)

        # Resize Buttons
        btn_states.resize(btn_states.sizeHint())
        btn_transitions.resize(btn_transitions.sizeHint())
        btn_roles.resize(btn_roles.sizeHint())

        # Move Buttons
        btn_states.move(0, 35)
        btn_transitions.move(0, 60)
        btn_roles.move(0, 85)

        # Click Event Connects/Calls
        btn_states.clicked.connect(self.click_states)
        btn_transitions.clicked.connect(self.click_transitions)
        btn_roles.clicked.connect(self.click_roles)

        # Add to Layout
        layout.addWidget(btn_states)
        layout.addWidget(btn_transitions)
        layout.addWidget(btn_roles)

    def action_buttons(self, layout):
        # Create Action Buttons
        btn_add = QPushButton('4.) Add', self)
        btn_remove = QPushButton('5.) Remove', self)
        btn_save = QPushButton('6.) Save', self)

        # Resize Action Buttons
        btn_add.resize(btn_add.sizeHint())
        btn_remove.resize(btn_remove.sizeHint())
        btn_save.resize(btn_save.sizeHint())

        # Move Action Buttons
        btn_add.move(50, 35)
        btn_remove.move(50, 60)
        btn_save.resize(50, 85)

        # Method Calls/Connects Action Buttons
        btn_add.clicked.connect(self.click_add)
        btn_save.clicked.connect(self.click_save)
        btn_remove.clicked.connect(self.click_remove)

        # Add Action Buttons to Widget
        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)
        layout.addWidget(btn_save)

    # Block for Click Events

    @pyqtSlot()
    # Swap Buttons
    def click_states(self):
        print('states clicked')
        self.hbox_table_widget.removeWidget(self.table_dict)
        self.current_dict = 'states'
        if len(self.states_dict) == 0:
            print("You Must Add an Item to This Dictionary")
            self.table_dict = QTableWidget()
        else:
            self.table_dict = self.dictionary_list_widget(self.states_dict)
        self.hbox_table_widget.addWidget(self.table_dict)

    def click_transitions(self):
        print('transitions clicked')
        self.hbox_table_widget.removeWidget(self.table_dict)
        self.current_dict = 'transitions'
        if len(self.transitions_dict) == 0:
            print("You Must Add an Item to This Dictionary")
            self.table_dict = QTableWidget()
        else:
            self.table_dict = self.dictionary_list_widget(self.transitions_dict)
        self.hbox_table_widget.addWidget(self.table_dict)

    def click_roles(self):
        print('quit clicked')

    # Action Buttons
    def click_add(self):
        print('add clicked')
        # Functionality:
        # Opens up a popup menu based on the current dictionary being viewed
        # Adds the entered values to the dictionary

        # Implementation:
        # 1.) Call to GUI_Workshop_Adding_Widget
        self.add_window = Workshop_Adding_GUI(self.current_dict)

        self.add_window.exec_()
        new_dict = self.add_window.new_item

        # 2.) Depending on what screen you are looking at, the method adds the new dict item to that dictionary
        if new_dict is None:
            print("No Input Given")
        else:
            if self.current_dict == 'states':
                self.states_dict.update(new_dict)
                self.click_states()
            elif self.current_dict == 'transitions':
                self.transitions_dict.update(new_dict)
                self.click_transitions()

    def click_remove(self):
        # Funcionality:
        # 1.) Select a Row and Click remove
        # 2.) Remove a row from table and rebuild dictionary to match removed entry
        print('remove clicked')
        if self.table_dict.currentRow() is None:
            print("Please Select an Item First")
        else:
            selected_item = self.table_dict.currentRow()
            if self.current_dict == 'states':
                self.states_dict = self.rebuild_dict(self.states_dict, selected_item)
                self.click_states()
            elif self.current_dict == 'transitions':
                self.transitions_dict = self.rebuild_dict(self.transitions_dict, selected_item)
                self.click_transitions()

        print('item removed')

    def click_save(self):
        save_dict('states', self.states_dict)
        save_dict('transitions', self.transitions_dict)
        print('Dictionaries Saved')

    # Reconstructs the dictionary for click_remove function
    def rebuild_dict(self, rebuild_dict, removing):
        # Deconstruct Old Dictionary
        dict_keys = []
        dict_values = []
        for key in rebuild_dict:
            item = rebuild_dict[key]
            dict_keys.append(key)
            dict_values.append(item)
        # Remove item that was removed
        dict_keys.pop(removing)
        dict_values.pop(removing)
        # Construct new Dictionary
        new_dict = {}
        for position in range(len(dict_keys)):
            new_item = {dict_keys[position]: dict_values[position]}
            new_dict.update(new_item)
        return new_dict
