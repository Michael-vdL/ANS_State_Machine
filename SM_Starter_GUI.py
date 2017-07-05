# Needed to inherit Resources

import sys
from gui.GUI_Application_Hub import *


def run_app():
    app = QApplication(sys.argv)
    ex = Application_Hub_GUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
