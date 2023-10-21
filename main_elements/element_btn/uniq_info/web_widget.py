from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic  # Импортируем uic


class WebWidget(widgets.QWidget):
    def __init__(self, s, data: str):
        super().__init__(s)
        uic.loadUi('static/web_widget.ui', self)

        self.s = s
        self.link = data

        # set static info
        self.setFixedHeight(131)
        self.setFixedWidth(210)
        self.show()
        self.setVisible(True)

        # set the defaults
        self.web_line_edit.setText(self.link)
        # connect the text changes
        self.web_line_edit.textChanged.connect(self.web_change)
        self.web_line_edit.editingFinished.connect(self.openUrl)  # for url
        # create a right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def openUrl(self):
        url = QUrl(self.web_line_edit.text())
        if not url.scheme():
            url.setScheme('http')
        QDesktopServices.openUrl(url)

    def web_change(self):
        self.link = self.web_line_edit.text()

    def showContextMenu(self, pos):  # delete the info
        contextMenu = QtWidgets.QMenu(self)
        open_link_action = contextMenu.addAction("Открыть ссылку")
        delete_action = contextMenu.addAction("Удалить серии")
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            self.s.data[8] = None
            self.deleteLater()
        if action == open_link_action:
            self.openUrl()

    def return_data(self):  # this foo is for the commit
        return f'web|{self.link}'
