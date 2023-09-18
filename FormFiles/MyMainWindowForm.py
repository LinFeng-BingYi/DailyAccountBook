from PySide6.QtWidgets import QMainWindow

from FormFiles.MyMainWindow import Ui_MyMainWindow
from FormFiles.EditAccountBookForm import WidgetEditAccountBook


class MainMyMainWindow(QMainWindow, Ui_MyMainWindow):
    def __init__(self):
        super(MainMyMainWindow, self).__init__()
        self.setupUi(self)

        self.editAccountBookForm = None

        self.bindSignal()

    def bindSignal(self):
        self.action_edit.triggered.connect(self.displayEditAccountBookForm)

    def displayEditAccountBookForm(self):
        self.editAccountBookForm = WidgetEditAccountBook()
        self.editAccountBookForm.show()
