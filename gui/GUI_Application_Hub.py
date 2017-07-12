#!/usr/bin/python

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from gui.GUI_Workshop_Hub import Workshop_Hub_GUI
from gui.GUI_Observer_Hub import Observer_Hub_GUI
from gui.GUI_Network_Map import Network_Map_GUI
from gui.GUI_Mininet_Hub import Mininet_Hub_GUI
from gui.GUI_Test_Hub import Test_Hub_GUI

from objects.SM_Observer import *


class Application_Hub_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Network State Machine - Main Window')
        self.setGeometry(100, 100, 720, 480)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initiate Observer
        self.obsv = Observer()

        # Instantiate Tabs
        self.tabs = QTabWidget()
        self.tab_observer = Observer_Hub_GUI(self.obsv)
        self.tab_workshop = Workshop_Hub_GUI()
        self.tab_test_center = Test_Hub_GUI(self.obsv)
        self.tab_network_map = Network_Map_GUI()
        self.tab_mininet = Mininet_Hub_GUI()
        self.tabs.resize(300, 200)

        # Add Tabs to Tab Widget
        self.tabs.addTab(self.tab_observer, "Observer")
        self.tabs.addTab(self.tab_workshop, "Workshop")
        self.tabs.addTab(self.tab_test_center, "Test Center")
        self.tabs.addTab(self.tab_network_map, "Network Map")
        self.tabs.addTab(self.tab_mininet, "Mininet")

        # Create Tab Layouts
        self.tab_observer.layout = QVBoxLayout(self)
        self.tab_observer.setLayout(self.tab_observer.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        # Add Layouts to top_layout
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
