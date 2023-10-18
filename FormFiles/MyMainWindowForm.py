from PySide6.QtWidgets import QMainWindow

from FormFiles.MyMainWindow import Ui_MyMainWindow
from FormFiles.EditAccountBookForm import WidgetEditAccountBook
from FormFiles.VisualiseAccountBookForm import WidgetVisualiseAccountBook


class MainMyMainWindow(QMainWindow, Ui_MyMainWindow):
    def __init__(self):
        super(MainMyMainWindow, self).__init__()
        self.setupUi(self)

        self.editAccountBookForm = None
        self.visualizeAccountBookForm = None

        self.bindSignal()

    def bindSignal(self):
        self.action_edit.triggered.connect(self.displayEditAccountBookForm)
        self.action_visualize.triggered.connect(self.displayVisualizeAccountBookForm)

    def displayEditAccountBookForm(self):
        self.editAccountBookForm = WidgetEditAccountBook()
        self.editAccountBookForm.show()

    def displayVisualizeAccountBookForm(self):
        self.visualizeAccountBookForm = WidgetVisualiseAccountBook()
        self.visualizeAccountBookForm.show()
