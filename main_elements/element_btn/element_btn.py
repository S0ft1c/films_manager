from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


# TODO: create a edit dialog


class ElementBtn(widgets.QLabel):
    def __init__(self, s, id):
        super().__init__()

        self.s = s  # mainwindow self
        self.id = id

        self.setFixedHeight(100)  # here is a fixed height of label

        data = db.get_element_by_id(self.id)
        if data:
            self.name = data[1]
            self.textcolor = data[2]
            self.backcolor = data[3]
            self.bordercolor = data[4]
            self.desc = data[10]

        # create a texts
        self.setText(self.name)
        self.setToolTip(self.desc)

        self.setStyleSheet('QLabel {' + f"""border: 4px solid {self.bordercolor};
                text-color: {self.textcolor};
                background-color: {self.backcolor};
                border-radius: 5px;
                font-family: 'Lato', sans-serif;
                font-weight: 500;
                font-size: 24;
                padding-left: 25px;""" + '}')

