from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QTableWidgetItem
from PySide6.QtCore import Qt, QDate

import os

from FormFiles.EditAccountBook import Ui_EditAccountBook

TABLEWIDGET_EXPENSE_COLUMN_HEAD = {'基本需求': 'necessity', '数值': 'value', '类别': 'category', '细则': 'detail', '描述': 'describe', '支出账户': 'from', '关联账户': 'associatedFund', '操作': ''}
TABLEWIDGET_INCOME_COLUMN_HEAD = {'数值': 'value', '类别': 'category', '细则': 'detail', '描述': 'describe', '收入账户': 'to', '关联账户': 'associatedFund', '操作': ''}
TABLEWIDGET_MOVEMENT_COLUMN_HEAD = {'数值': 'value', '细则': 'detail', '描述': 'describe', '转出账户': 'from', '转入账户': 'to', '操作': ''}


class WidgetEditAccountBook(QWidget, Ui_EditAccountBook):

    def __init__(self):
        super(WidgetEditAccountBook, self).__init__()
        self.setupUi(self)
        self.tableWidget_expense.setColumnCount(len(TABLEWIDGET_EXPENSE_COLUMN_HEAD))
        self.tableWidget_expense.setHorizontalHeaderLabels(list(TABLEWIDGET_EXPENSE_COLUMN_HEAD))
        self.tableWidget_income.setColumnCount(len(TABLEWIDGET_INCOME_COLUMN_HEAD))
        self.tableWidget_income.setHorizontalHeaderLabels(list(TABLEWIDGET_INCOME_COLUMN_HEAD))
        self.tableWidget_movement.setColumnCount(len(TABLEWIDGET_MOVEMENT_COLUMN_HEAD))
        self.tableWidget_movement.setHorizontalHeaderLabels(list(TABLEWIDGET_MOVEMENT_COLUMN_HEAD))

        self.cwd = os.getcwd()              # 程序当前工作目录

        self.initWidgets()
        self.bindSignal()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def bindSignal(self):
        # 为各控件绑定信号与槽函数
        self.pushButton_file_path.clicked.connect(self.chooseFile)
        self.groupBox_expense.clicked.connect(lambda: self.widget_expense.setVisible(not self.widget_expense.isVisible()))
        self.groupBox_income.clicked.connect(lambda: self.widget_income.setVisible(not self.widget_income.isVisible()))
        self.groupBox_movement.clicked.connect(lambda: self.widget_movement.setVisible(not self.widget_movement.isVisible()))

    def initWidgets(self):
        # 为控件设置初始值
        self.dateEdit.setDate(QDate.currentDate())

    def chooseFile(self):
        chosen_file, file_type = QFileDialog.getOpenFileName(self, "选择文件", self.cwd, "All Files(*);;XML Files(*.xml)")
        self.lineEdit_file_path.setText(chosen_file)

