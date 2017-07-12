# Popup Window Widget that allows you to add states or transitions
# Finished:
# 1.) Popup window that takes input and returns it to the proper dictionary in Workshop_Hub
# 2.) Error for No Selected Dictionary
# Still Needed:
# 1.) Error handling to manage improper input
# 2.) Drop down window for type, maybe for selecting already available destination?

# !/usr/bin/python

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QApplication, QDialog

from gui.GUI_Workshop_Hub import *


class Workshop_Adding_GUI(QDialog):
    def __init__(self, current_dict):
        super().__init__()

        # Tracking Variables
        self.current_dict = current_dict
        self.new_item = None

        # Create Layouts --> Current Approach = Form Layout w/ Rows of Labels and Line Edits
        top_layout = QVBoxLayout()
        input_layout = QFormLayout()
        exit_options_layout = QHBoxLayout()

        # Layout Management
        if self.current_dict is None:  # In case the add option is selected before a dictionary is viewed
            input_layout.addRow(QLabel('No Dictionary Selected'))
        elif self.current_dict is 'states':
            self.init_states(input_layout)  # input_layout designed based on current window
        elif self.current_dict is 'transitions':
            self.init_transition(input_layout)
        top_layout.addLayout(input_layout)
        top_layout.addLayout(exit_options_layout)

        # Exit Option Buttons
        if self.current_dict is None:
            self.btn_ok = QPushButton('Ok', self)  # Instantiate
            self.btn_ok.resize(self.btn_ok.sizeHint())  # Resize
            exit_options_layout.addWidget(self.btn_ok)  # Add
            self.btn_ok.clicked.connect(self.click_cancel)  # Connect
        else:
            # Instantiate
            self.btn_enter = QPushButton('Enter', self)
            self.btn_cancel = QPushButton('Cancel', self)
            # Resize
            self.btn_enter.resize(self.btn_enter.sizeHint())
            self.btn_cancel.resize(self.btn_cancel.sizeHint())
            # Add
            exit_options_layout.addWidget(self.btn_enter)
            exit_options_layout.addWidget(self.btn_cancel)
            # Connect
            self.btn_enter.clicked.connect(self.click_enter)
            self.btn_cancel.clicked.connect(self.click_cancel)

        # Geometry and Layout
        self.setLayout(top_layout)
        self.setWindowTitle('...Adding {}...'.format(current_dict))

    def init_states(self, layout):
        # Create Labels
        self.lbl_name = QLabel("Enter Name: ")
        self.lbl_type = QLabel("Enter Type: ")
        self.lbl_func = QLabel("Enter Functions: ")
        self.lbl_trans = QLabel("Enter Transitions: ")

        # Create Line Edits
        self.le_name = QLineEdit()
        self.le_type = QLineEdit()
        self.le_func = QLineEdit()
        self.le_trans = QLineEdit()

        # Adding to Form Layout (form_layout.addRow(label, line_edit) <- This is the syntax
        layout.addRow(self.lbl_name, self.le_name)
        layout.addRow(self.lbl_type, self.le_type)
        layout.addRow(self.lbl_func, self.le_func)
        layout.addRow(self.lbl_trans, self.le_trans)

    def init_transition(self, layout):
        # Create Labels
        self.lbl_name = QLabel("Enter Name: ")
        self.lbl_dest = QLabel("Enter Destination: ")
        self.lbl_func = QLabel("Enter Function: ")

        # Create Line Edits
        self.le_name = QLineEdit()
        self.le_dest = QLineEdit()
        self.le_func = QLineEdit()

        # Adding to Form Layout (form_layout.addRow(label, line_edit) <- This is the syntax
        layout.addRow(self.lbl_name, self.le_name)
        layout.addRow(self.lbl_dest, self.le_dest)
        layout.addRow(self.lbl_func, self.le_func)

    def click_enter(self):
        # Functionality:
        # 1.) Checks if all information entered is valid and fits format
        # 2.) Makes new dictionary item
        # 2.) Closes window, sends new dictionary item to Workshop_hub dicts

        # Implementation:
        # 1.) Error Checks --> Do Later

        # 2.) Makes a dictionary item
        # Known Issue: Hard Coded for States, Must work for any, may need another method for other objects
        if self.current_dict is 'states':
            new_name = self.le_name.text()
            new_type = self.le_type.text()
            new_func = self.le_func.text().replace(' ', '').split(',')
            new_trans = self.le_trans.text().replace(' ', '').split(',')
            self.new_item = {new_name: {'type': new_type, 'func_perms': new_func, 'trans_perms': new_trans}}
        elif self.current_dict is 'transitions':
            new_name = self.le_name.text()
            new_dest = self.le_dest.text()
            new_func = self.le_func.text()
            self.new_item = {new_name: {'dest': new_dest, 'func': new_func}}

        # 2.) self.close() should shut window down
        # print(self.new_item)
        self.close()

    def click_cancel(self):
        print("Cancel Clicked")
        self.close()


def main():
    app = QApplication(sys.argv)
    ex = Workshop_Adding_GUI()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
