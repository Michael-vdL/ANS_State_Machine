from gui.GUI_Application_Hub import *
from api.routines.user_routines import routine_handler
import json


def get_routine_dict():
    with open('resources/routines.json') as resource_file:
        dict = json.load(resource_file)
    return dict


class Routines_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        self.top_layout = QHBoxLayout()

        # List
        self.top_layout.addWidget(Routines_List(self.obsv), 1)
        self.top_layout.addWidget(QTableWidget(), 3)
        # Edit Pane

        self.setLayout(self.top_layout)


class Routines_List(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.routine_dict = get_routine_dict()
        self.initUI()

    def initUI(self):
        self.list_layout = QVBoxLayout()  # List and a Description Box that loads details from a routine

        self.routine_lst = QListWidget()
        self.initList()

        self.detail_grp_box = QGroupBox()
        self.btn_run = QPushButton("Run", self)
        self.btn_run.resize(self.btn_run.sizeHint())
        self.btn_run.clicked.connect(self.click_run)

        self.list_layout.addWidget(self.routine_lst)
        self.list_layout.addWidget(self.detail_grp_box)
        self.list_layout.addWidget(self.btn_run)
        self.setLayout(self.list_layout)

    def initList(self):
        for routine in self.routine_dict:
            lst_item = QListWidgetItem(routine)
            self.routine_lst.addItem(lst_item)

    def initDetails(self):

        lbl_name = QLabel("Name: ")
        lbl_description = QLabel("Description: ")
        lbl_routine_count = QLabel("Number of Steps: ")

    def click_run(self):
        for device in self.obsv.device_session_status['open']:
            routine_handler(device.session, self.routine_lst.currentItem().text())
