from PySide6.QtWidgets import QWidget, QComboBox


class ComboBoxInTableWidget(QComboBox):
    def __init__(self, item_dict: dict, init_key, parent=None):
        super().__init__(parent)

        # 该控件的项列表
        self.item_dict = item_dict

        if len(item_dict) != 0:
            self.initWidgets(init_key)

    def initWidgets(self, init_key):
        """
        Describe: 初始化自定义ComboBox控件

        Args:
            init_key: Any
                init_key的类型与self.item_dict键的类型一致，是该字典的一个键。
        """
        # 设置视图最小宽度
        self.view().setMinimumWidth(150)

        # 初始化列表，并设置初值
        self.addItems(list(self.item_dict.values()))
        # print(list(self.item_dict))
        init_index = list(self.item_dict).index(init_key)
        self.setCurrentIndex(init_index)

    def getKeyByCurrentText(self):
        """
        Describe:
            由于显示给用户的数据与记录于文件的数据不同，因此，通过该方法找出对应的键值对

        Returns: Any
            返回当前文本对应的用于写入文件的键
            example:
            ...
        """
        for k, v in self.item_dict.items():
            if v == self.currentText():
                return k
