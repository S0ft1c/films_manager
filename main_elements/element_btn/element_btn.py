from PyQt5 import QtWidgets as widgets
from PyQt5 import QtWidgets

from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from .element_edit_dialog import EditElementDialog


class ElementBtn(widgets.QLabel):
    def __init__(self, s, id):
        super().__init__()

        self.s = s  # mainwindow self
        self.id = id

        self.setFixedHeight(100)  # here is a fixed height of label

        data = db.get_element_by_id(self.id)
        if data:
            self.name = data[1]
            self.textcolor = data[3]
            self.backcolor = data[4]
            self.bordercolor = data[5]
            self.category_id = data[2]
            self.desc = data[10]

        # create a texts
        self.setText(self.name)
        self.setToolTip(self.desc)

        self.setStyleSheet('QLabel {' + f"""border: 4px solid {self.bordercolor};
                color: {self.textcolor};
                background-color: {self.backcolor};
                border-radius: 5px;
                font-weight: 500;
                font-family: 'Times', sans-serif;
                font-size: 24;
                padding-left: 25px;""" + '}')
        self.setFont(QtGui.QFont("Lato", 16, QtGui.QFont.Bold))
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # connect the mousePressEvent
        self.mousePressEvent = self.left_click

        # create a right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        contextMenu = QtWidgets.QMenu(self)
        delete_action = contextMenu.addAction("Удалить элемент")
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == delete_action:  # if we want to delete
            db.delete_element(self.id)
            self.s.elements_load_data(self.category_id)

    def left_click(self, event):
        if event.button() == Qt.LeftButton:
            dialog = EditElementDialog(self, self.id)
            dialog.exec_()
