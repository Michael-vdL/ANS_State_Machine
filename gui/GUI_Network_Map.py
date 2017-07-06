from gui.GUI_Application_Hub import *


class Network_Map_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.node_list = []
