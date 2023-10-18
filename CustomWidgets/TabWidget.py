
from PySide6.QtWidgets import QTabWidget, QTabBar


class FormTabBar(QTabBar):
    """
    Describe:
        自定义QTabWidget标签形式
    """
    def tabSizeHint(self, index):
        """
        Describe:
            修改标签的宽和高，宽和高的方向不会因位置的改变而交换
        """
        size = QTabBar.tabSizeHint(self, index)
        size.setWidth(50)  # Set the width of the tab
        size.setHeight(100)
        return size
