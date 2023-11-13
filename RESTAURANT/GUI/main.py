import sys

from PyQt6.QtWidgets import QApplication as app
from login import Login

current_user = None

if __name__ == '__main__':
    desktop = app(sys.argv)
    login_form = Login()
    login_form.show()
    desktop.exec()