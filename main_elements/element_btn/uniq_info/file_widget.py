from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic  # Импортируем uic
import os
import subprocess


class FileWidget(widgets.QWidget):
    def __init__(self, s, data: str):
        super().__init__(s)
        uic.loadUi('static/file_widget.ui', self)

        self.s = s
        self.file = data

        # set static info
        self.setFixedHeight(131)
        self.setFixedWidth(210)
        self.show()
        self.setVisible(True)

        # set the defaults
        self.file_btn.setText(self.file.split('/')[-1])
        # set the clicked connect
        self.file_btn.clicked.connect(
            self.start_file
        )
        # create a right-click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def start_file(self):
        full_path = os.path.abspath(self.file)
        os.startfile(full_path)

    def showContextMenu(self, pos):  # delete the info
        contextMenu = QtWidgets.QMenu(self)
        open_in_folder = contextMenu.addAction("Открыть в проводнике")
        delete_action = contextMenu.addAction("Удалить файл")
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == delete_action:
            prompt_arr = self.s.data[9].split(', ').copy()
            prompt_arr.remove(self.file)
            self.s.data[9] = ', '.join(prompt_arr)
            os.remove(self.file)  # rm file from cache
            self.deleteLater()
        if action == open_in_folder:
            full_path = os.path.abspath(self.file)
            subprocess.Popen(f'explorer /select,"{full_path}"')

    def return_data(self):  # this foo is for the commit
        return f'file|{self.file}'
