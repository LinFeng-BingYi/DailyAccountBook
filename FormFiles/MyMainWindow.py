# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MyMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QToolBar,
    QWidget)

class Ui_MyMainWindow(object):
    def setupUi(self, MyMainWindow):
        if not MyMainWindow.objectName():
            MyMainWindow.setObjectName(u"MyMainWindow")
        MyMainWindow.resize(600, 350)
        MyMainWindow.setMinimumSize(QSize(600, 350))
        MyMainWindow.setMaximumSize(QSize(600, 350))
        MyMainWindow.setIconSize(QSize(25, 25))
        MyMainWindow.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.action_edit = QAction(MyMainWindow)
        self.action_edit.setObjectName(u"action_edit")
        self.action_visualize = QAction(MyMainWindow)
        self.action_visualize.setObjectName(u"action_visualize")
        self.action_style = QAction(MyMainWindow)
        self.action_style.setObjectName(u"action_style")
        self.action_global_config = QAction(MyMainWindow)
        self.action_global_config.setObjectName(u"action_global_config")
        self.action_tutorial = QAction(MyMainWindow)
        self.action_tutorial.setObjectName(u"action_tutorial")
        self.action_about = QAction(MyMainWindow)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(MyMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(590, 260))

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        MyMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MyMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 22))
        self.menubar.setMinimumSize(QSize(0, 20))
        self.menubar.setNativeMenuBar(True)
        self.menu_function = QMenu(self.menubar)
        self.menu_function.setObjectName(u"menu_function")
        self.menu_function.setGeometry(QRect(200, 127, 120, 90))
        self.menu_function.setMinimumSize(QSize(120, 0))
        self.menu_setting = QMenu(self.menubar)
        self.menu_setting.setObjectName(u"menu_setting")
        self.menu_setting.setMinimumSize(QSize(120, 0))
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MyMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MyMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setMinimumSize(QSize(0, 20))
        MyMainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MyMainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(0, 0))
        self.toolBar.setMovable(True)
        MyMainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_function.menuAction())
        self.menubar.addAction(self.menu_setting.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_function.addAction(self.action_edit)
        self.menu_function.addAction(self.action_visualize)
        self.menu_setting.addAction(self.action_style)
        self.menu_setting.addAction(self.action_global_config)
        self.menu_help.addAction(self.action_tutorial)
        self.menu_help.addAction(self.action_about)
        self.toolBar.addAction(self.action_edit)
        self.toolBar.addAction(self.action_visualize)
        self.toolBar.addAction(self.action_global_config)
        self.toolBar.addAction(self.action_tutorial)
        self.toolBar.addAction(self.action_about)

        self.retranslateUi(MyMainWindow)

        QMetaObject.connectSlotsByName(MyMainWindow)
    # setupUi

    def retranslateUi(self, MyMainWindow):
        MyMainWindow.setWindowTitle(QCoreApplication.translate("MyMainWindow", u"\u6797\u98ce\u51b0\u7ffc\u7684\u65e5\u5e38\u8d26\u672c", None))
        self.action_edit.setText(QCoreApplication.translate("MyMainWindow", u"\u7f16\u8f91\u8d26\u672c", None))
        self.action_visualize.setText(QCoreApplication.translate("MyMainWindow", u"\u53ef\u89c6\u5316\u8d26\u672c", None))
        self.action_style.setText(QCoreApplication.translate("MyMainWindow", u"\u7a97\u53e3\u98ce\u683c", None))
        self.action_global_config.setText(QCoreApplication.translate("MyMainWindow", u"\u5168\u5c40\u914d\u7f6e", None))
        self.action_tutorial.setText(QCoreApplication.translate("MyMainWindow", u"\u4f7f\u7528\u6559\u7a0b", None))
        self.action_about.setText(QCoreApplication.translate("MyMainWindow", u"\u5173\u4e8e", None))
        self.menu_function.setTitle(QCoreApplication.translate("MyMainWindow", u"\u529f\u80fd", None))
        self.menu_setting.setTitle(QCoreApplication.translate("MyMainWindow", u"\u8bbe\u7f6e", None))
        self.menu_help.setTitle(QCoreApplication.translate("MyMainWindow", u"\u5e2e\u52a9", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MyMainWindow", u"toolBar", None))
    # retranslateUi

