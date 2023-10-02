from PyQt5 import QtWidgets as widgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from .add_category_dialog import AddCategoryDialog

style = """
  color: #fff;
  width: 300px;
  height: 80px;
  border-radius: 5px;
  font-family: 'Lato', sans-serif;
  font-weight: 500;
  background: rgb(96,9,240);
  font-size: 20;
"""


class AddCategoryBtn(widgets.QPushButton):
    def __init__(self, s):
        super().__init__(s)

        self.initUI()

    def initUI(self):
        # here write a name of file we needed
        self.setStyleSheet(style)

        # set a text of a btn
        self.setText('Создать категорию')

        # resize
        self.resize(self.sizeHint())

        # here write a foo on the connector
        self.clicked.connect(self.clicked_btn)

    def clicked_btn(self):
        dialog = AddCategoryDialog()
        dialog.exec_()
