# Needed to inherit Resources
# !/usr/bin/python

import sys
from gui.GUI_Application_Hub import *
from bin.junos_information_collector import *

def run_app():
    app = QApplication(sys.argv)
    ex = Application_Hub_GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # information_collector() #Disable so testing doesn't take a year to load
    run_app()
