from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic  # Импортируем uic


class LastPageWidget(widgets.QWidget):
    def __init__(self, s, data: str):
        super().__init__(s)
        uic.loadUi('static/last_page_widget.ui', self)

        self.s = s
        self.page = data

        # set static info
        self.setFixedHeight(131)
        self.setFixedWidth(210)
        self.show()
        self.setVisible(True)

        # set the defaults
        self.last_page_line_edit.setText(str(self.page))
        # set the change text
        self.last_page_line_edit.textChanged.connect(self.page_changed)

        # create a right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):  # delete the info
        contextMenu = QtWidgets.QMenu(self)
        delete_action = contextMenu.addAction("Удалить страницу")
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            self.s.data[7] = None
            self.deleteLater()

    def page_changed(self):
        self.page = self.last_page_line_edit.text().strip()

    def return_data(self):  # this foo is for the commit
        return f'last_page|{self.page}'
