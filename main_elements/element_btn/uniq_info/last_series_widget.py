from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic  # Импортируем uic


class LastSeriesWidget(widgets.QWidget):
    def __init__(self, s, data: str):
        super().__init__(s)
        uic.loadUi('static/last_series_widget.ui', self)

        self.s = s
        self.season, self.seria = data.split(', ')

        # set static info
        self.setFixedHeight(131)
        self.setFixedWidth(210)
        self.show()
        self.setVisible(True)

        # set the defaults
        self.season_line_edit.setText(self.season)
        self.series_line_edit.setText(self.seria)

        # connect the text changes
        self.season_line_edit.textChanged.connect(self.change_season)
        self.series_line_edit.textChanged.connect(self.change_seria)

        # create a right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):  # delete the info
        contextMenu = QtWidgets.QMenu(self)
        delete_action = contextMenu.addAction("Удалить серии")
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            self.s.data[6] = None
            self.deleteLater()

    def change_season(self):
        self.season = self.season_line_edit.text()

    def change_seria(self):
        self.seria = self.series_line_edit.text()

    def return_data(self):  # this foo is for the commit
        return f'last_series-{self.season}, {self.seria}'
