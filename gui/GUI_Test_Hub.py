from gui.GUI_Application_Hub import *
from objects.SM_Observer import *
from random import randint as r

# !/usr/bin/python

class Test_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        self.top_layout = QVBoxLayout()
        self.tmp_list_widget = None  # Temporary item until we find a better place for alerts
        # Add Test Buttons
        btn_run_transition_test = QPushButton('Run Transition Test', self)
        btn_run_exit_quarantine_test = QPushButton('Exit Quarantine Test', self)
        btn_display_alerts = QPushButton('Display Alerts', self)
        # Resize Test Buttons
        btn_run_transition_test.resize(btn_run_transition_test.sizeHint())
        btn_run_exit_quarantine_test.resize(btn_run_exit_quarantine_test.sizeHint())
        btn_display_alerts.resize(btn_display_alerts.sizeHint())
        # Connect Test Buttons
        btn_run_transition_test.clicked.connect(self.click_run_transition_test)
        btn_run_exit_quarantine_test.clicked.connect(self.click_run_exit_quarantine_test)
        btn_display_alerts.clicked.connect(self.click_display_alerts)
        # Add Buttons to Layout
        self.top_layout.addWidget(btn_run_transition_test)
        self.top_layout.addWidget(btn_run_exit_quarantine_test)
        self.top_layout.addWidget(btn_display_alerts)
        # Geometry and Layout
        self.setLayout(self.top_layout)

    def click_run_transition_test(self):
        for state in self.obsv.states:
            if len(state.nodes_in_state) > 0:
                node = state.nodes_in_state[r(0, len(state.nodes_in_state))]
                transition = self.obsv.transitions[r(0, len(self.obsv.transitions) - 1)]
                self.obsv.run_transition(state, node, transition)
                return

    def click_run_exit_quarantine_test(self):
        for state in self.obsv.states:
            if state.name == 'Quarantine':
                transition = self.obsv.transitions[0]
                for node in state.nodes_in_state:
                    self.obsv.run_transition(state, node, transition)

    def click_display_alerts(self):
        if self.tmp_list_widget:
            self.top_layout.removeWidget(self.tmp_list_widget)
            self.tmp_list_widget = None
        self.tmp_list_widget = QListWidget()
        for change in self.obsv.changes:
            list_item = QListWidgetItem(change)
            self.tmp_list_widget.addItem(list_item)
        self.top_layout.addWidget(self.tmp_list_widget)
