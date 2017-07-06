from gui.GUI_Application_Hub import *
from objects.SM_Observer import *


class Test_Hub_GUI(QWidget):
    def __init__(self, observer):
        super().__init__()
        self.obsv = observer
        self.initUI()

    def initUI(self):
        self.top_layout = QVBoxLayout()

        # Add Test Buttons
        btn_add_node_test = QPushButton('Add Node Test', self)
        btn_run_transition_test = QPushButton('Run Transition Test', self)

        # Resize Test Buttons
        btn_add_node_test.resize(btn_add_node_test.sizeHint())
        btn_run_transition_test.resize(btn_run_transition_test.sizeHint())

        # Connect Test Buttons
        btn_add_node_test.clicked.connect(self.click_add_node_test)
        btn_run_transition_test.clicked.connect(self.click_run_transition_test)

        # Add Buttons to Layout
        self.top_layout.addWidget(btn_add_node_test)
        self.top_layout.addWidget(btn_run_transition_test)

        # Geometry and Layout
        self.setLayout(self.top_layout)

    def click_add_node_test(self):
        from random import randint as r
        for state in self.obsv.states:
            if state.type == 'start':
                num_of_nodes = r(0, 10)
                for i in range(num_of_nodes):
                    state.add_node('h{}'.format(len(state.nodes_in_state)))
                    print('added nodes')

    def click_run_transition_test(self):
        from random import randint as r
        for state in self.obsv.states:
            print("Possibly 5")
            if len(state.nodes_in_state) > 0:
                print("Possibly 6")
                node = state.nodes_in_state[r(0, len(state.nodes_in_state))]
                print("Possibly 7")
                transition = self.obsv.transitions[0]
                print("Possibly 8")
                self.obsv.run_transition(state, node, transition)
                print("Possibly 9")
                return
