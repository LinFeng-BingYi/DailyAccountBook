# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditAccountBook.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_EditAccountBook(object):
    def setupUi(self, EditAccountBook):
        if not EditAccountBook.objectName():
            EditAccountBook.setObjectName(u"EditAccountBook")
        EditAccountBook.resize(950, 600)
        self.gridLayout_top = QGridLayout(EditAccountBook)
        self.gridLayout_top.setSpacing(0)
        self.gridLayout_top.setObjectName(u"gridLayout_top")
        self.gridLayout_top.setContentsMargins(0, 0, 0, 0)
        self.widget_general = QWidget(EditAccountBook)
        self.widget_general.setObjectName(u"widget_general")
        self.widget_general.setMinimumSize(QSize(950, 600))
        self.verticalLayout_general = QVBoxLayout(self.widget_general)
        self.verticalLayout_general.setObjectName(u"verticalLayout_general")
        self.widget_file_path = QWidget(self.widget_general)
        self.widget_file_path.setObjectName(u"widget_file_path")
        self.horizontalLayout_file_path = QHBoxLayout(self.widget_file_path)
        self.horizontalLayout_file_path.setSpacing(10)
        self.horizontalLayout_file_path.setObjectName(u"horizontalLayout_file_path")
        self.horizontalLayout_file_path.setContentsMargins(10, 10, 10, 10)
        self.label_file_path = QLabel(self.widget_file_path)
        self.label_file_path.setObjectName(u"label_file_path")
        self.label_file_path.setMinimumSize(QSize(50, 30))
        self.label_file_path.setMaximumSize(QSize(50, 30))

        self.horizontalLayout_file_path.addWidget(self.label_file_path)

        self.lineEdit_file_path = QLineEdit(self.widget_file_path)
        self.lineEdit_file_path.setObjectName(u"lineEdit_file_path")
        self.lineEdit_file_path.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_file_path.addWidget(self.lineEdit_file_path)

        self.pushButton_file_path = QPushButton(self.widget_file_path)
        self.pushButton_file_path.setObjectName(u"pushButton_file_path")
        self.pushButton_file_path.setMinimumSize(QSize(80, 30))
        self.pushButton_file_path.setMaximumSize(QSize(80, 30))

        self.horizontalLayout_file_path.addWidget(self.pushButton_file_path)


        self.verticalLayout_general.addWidget(self.widget_file_path)

        self.widget_date = QWidget(self.widget_general)
        self.widget_date.setObjectName(u"widget_date")
        self.horizontalLayout = QHBoxLayout(self.widget_date)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.label_date = QLabel(self.widget_date)
        self.label_date.setObjectName(u"label_date")
        self.label_date.setMinimumSize(QSize(50, 30))
        self.label_date.setMaximumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.label_date)

        self.dateEdit = QDateEdit(self.widget_date)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setMinimumSize(QSize(0, 30))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setTimeSpec(Qt.LocalTime)

        self.horizontalLayout.addWidget(self.dateEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)

        self.verticalLayout_general.addWidget(self.widget_date)

        self.scrollArea = QScrollArea(self.widget_general)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 913, 815))
        self.verticalLayout_scrollArea = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_scrollArea.setSpacing(5)
        self.verticalLayout_scrollArea.setObjectName(u"verticalLayout_scrollArea")
        self.verticalLayout_scrollArea.setContentsMargins(0, 5, 0, 5)
        self.groupBox_expense = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_expense.setObjectName(u"groupBox_expense")
        self.groupBox_expense.setMinimumSize(QSize(0, 0))
        self.groupBox_expense.setFlat(True)
        self.groupBox_expense.setCheckable(True)
        self.gridLayout_expense = QGridLayout(self.groupBox_expense)
        self.gridLayout_expense.setSpacing(0)
        self.gridLayout_expense.setObjectName(u"gridLayout_expense")
        self.gridLayout_expense.setContentsMargins(18, 0, 0, 0)
        self.widget_expense = QWidget(self.groupBox_expense)
        self.widget_expense.setObjectName(u"widget_expense")
        self.widget_expense.setMinimumSize(QSize(720, 250))
        self.gridLayout_expense_widget = QGridLayout(self.widget_expense)
        self.gridLayout_expense_widget.setSpacing(0)
        self.gridLayout_expense_widget.setObjectName(u"gridLayout_expense_widget")
        self.gridLayout_expense_widget.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_expense = QTableWidget(self.widget_expense)
        self.tableWidget_expense.setObjectName(u"tableWidget_expense")

        self.gridLayout_expense_widget.addWidget(self.tableWidget_expense, 1, 0, 1, 1)

        self.label_expense_table = QLabel(self.widget_expense)
        self.label_expense_table.setObjectName(u"label_expense_table")
        self.label_expense_table.setMinimumSize(QSize(0, 25))

        self.gridLayout_expense_widget.addWidget(self.label_expense_table, 0, 0, 1, 1)


        self.gridLayout_expense.addWidget(self.widget_expense, 0, 0, 1, 1)


        self.verticalLayout_scrollArea.addWidget(self.groupBox_expense)

        self.groupBox_income = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_income.setObjectName(u"groupBox_income")
        self.groupBox_income.setMinimumSize(QSize(0, 0))
        self.groupBox_income.setFlat(True)
        self.groupBox_income.setCheckable(True)
        self.gridLayout_income = QGridLayout(self.groupBox_income)
        self.gridLayout_income.setSpacing(0)
        self.gridLayout_income.setObjectName(u"gridLayout_income")
        self.gridLayout_income.setContentsMargins(18, 0, 0, 0)
        self.widget_income = QWidget(self.groupBox_income)
        self.widget_income.setObjectName(u"widget_income")
        self.widget_income.setMinimumSize(QSize(720, 250))
        self.gridLayout_income_widget = QGridLayout(self.widget_income)
        self.gridLayout_income_widget.setSpacing(0)
        self.gridLayout_income_widget.setObjectName(u"gridLayout_income_widget")
        self.gridLayout_income_widget.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_income = QTableWidget(self.widget_income)
        self.tableWidget_income.setObjectName(u"tableWidget_income")

        self.gridLayout_income_widget.addWidget(self.tableWidget_income, 1, 0, 1, 1)

        self.label_income_table = QLabel(self.widget_income)
        self.label_income_table.setObjectName(u"label_income_table")
        self.label_income_table.setMinimumSize(QSize(0, 25))

        self.gridLayout_income_widget.addWidget(self.label_income_table, 0, 0, 1, 1)


        self.gridLayout_income.addWidget(self.widget_income, 0, 0, 1, 1)


        self.verticalLayout_scrollArea.addWidget(self.groupBox_income)

        self.groupBox_movement = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_movement.setObjectName(u"groupBox_movement")
        self.groupBox_movement.setMinimumSize(QSize(0, 0))
        self.groupBox_movement.setFlat(True)
        self.groupBox_movement.setCheckable(True)
        self.gridLayout_movement = QGridLayout(self.groupBox_movement)
        self.gridLayout_movement.setSpacing(0)
        self.gridLayout_movement.setObjectName(u"gridLayout_movement")
        self.gridLayout_movement.setContentsMargins(18, 0, 0, 0)
        self.widget_movement = QWidget(self.groupBox_movement)
        self.widget_movement.setObjectName(u"widget_movement")
        self.widget_movement.setMinimumSize(QSize(720, 250))
        self.gridLayout_movement_widget = QGridLayout(self.widget_movement)
        self.gridLayout_movement_widget.setSpacing(0)
        self.gridLayout_movement_widget.setObjectName(u"gridLayout_movement_widget")
        self.gridLayout_movement_widget.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_movement = QTableWidget(self.widget_movement)
        self.tableWidget_movement.setObjectName(u"tableWidget_movement")

        self.gridLayout_movement_widget.addWidget(self.tableWidget_movement, 1, 0, 1, 1)

        self.label_movement_table = QLabel(self.widget_movement)
        self.label_movement_table.setObjectName(u"label_movement_table")
        self.label_movement_table.setMinimumSize(QSize(0, 25))

        self.gridLayout_movement_widget.addWidget(self.label_movement_table, 0, 0, 1, 1)


        self.gridLayout_movement.addWidget(self.widget_movement, 0, 0, 1, 1)


        self.verticalLayout_scrollArea.addWidget(self.groupBox_movement)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_general.addWidget(self.scrollArea)

        self.verticalLayout_general.setStretch(0, 1)
        self.verticalLayout_general.setStretch(1, 1)
        self.verticalLayout_general.setStretch(2, 9)

        self.gridLayout_top.addWidget(self.widget_general, 0, 0, 1, 1)


        self.retranslateUi(EditAccountBook)

        QMetaObject.connectSlotsByName(EditAccountBook)
    # setupUi

    def retranslateUi(self, EditAccountBook):
        EditAccountBook.setWindowTitle(QCoreApplication.translate("EditAccountBook", u"\u7f16\u8f91\u8d26\u672c", None))
        self.label_file_path.setText(QCoreApplication.translate("EditAccountBook", u"\u6587\u4ef6\u8def\u5f84", None))
        self.pushButton_file_path.setText(QCoreApplication.translate("EditAccountBook", u"\u6d4f\u89c8", None))
        self.label_date.setText(QCoreApplication.translate("EditAccountBook", u"\u65e5    \u671f", None))
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("EditAccountBook", u"yyyy/MM/dd", None))
        self.groupBox_expense.setTitle(QCoreApplication.translate("EditAccountBook", u"\u652f\u51fa", None))
        self.label_expense_table.setText(QCoreApplication.translate("EditAccountBook", u"\u652f\u51fa\u8bb0\u5f55", None))
        self.groupBox_income.setTitle(QCoreApplication.translate("EditAccountBook", u"\u6536\u5165", None))
        self.label_income_table.setText(QCoreApplication.translate("EditAccountBook", u"\u6536\u5165\u8bb0\u5f55", None))
        self.groupBox_movement.setTitle(QCoreApplication.translate("EditAccountBook", u"\u8f6c\u79fb", None))
        self.label_movement_table.setText(QCoreApplication.translate("EditAccountBook", u"\u8f6c\u79fb\u8bb0\u5f55", None))
    # retranslateUi

