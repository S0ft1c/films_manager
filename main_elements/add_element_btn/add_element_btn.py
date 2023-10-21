from PyQt5 import QtWidgets as widgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from .add_element_dialog import AddElementDialog


class AddElementBtn:
    def __init__(self, s, category_id: int):
        self.category_id = category_id
        self.s = s

    def create_element(self):
        dialog = AddElementDialog(self.s, self.category_id)
        dialog.exec_()
