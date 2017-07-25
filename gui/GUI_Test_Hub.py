from gui.GUI_Application_Hub import *
from objects.SM_Observer import *


# !/usr/bin/python

class Test_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        self.top_layout = QVBoxLayout()

        # Add Test Buttons
        btn_run_transition_test = QPushButton('Run Transition Test', self)

        # Resize Test Buttons
        btn_run_transition_test.resize(btn_run_transition_test.sizeHint())

        # Connect Test Buttons
        btn_run_transition_test.clicked.connect(self.click_run_transition_test)

        # Add Buttons to Layout
        self.top_layout.addWidget(btn_run_transition_test)

        # Geometry and Layout
        self.setLayout(self.top_layout)

    def click_run_transition_test(self):
        from random import randint as r
        for state in self.obsv.states:
            if len(state.nodes_in_state) > 0:
                node = state.nodes_in_state[r(0, len(state.nodes_in_state))]
                transition = self.obsv.transitions[0]
                self.obsv.run_transition(state, node, transition)
                return
