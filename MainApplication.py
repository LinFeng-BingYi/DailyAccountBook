from PySide6.QtWidgets import QApplication

from FormFiles.MyMainWindowForm import MainMyMainWindow


if __name__ == '__main__':
    app = QApplication([])
    myMainWindow = MainMyMainWindow()
    myMainWindow.show()
    app.exec()
