from PyQt5 import QtWidgets as widgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5 import uic  # Импортируем uic
from db_class import db


class AddElementDialog(widgets.QDialog):
    def __init__(self, category_id):
        super().__init__()

        uic.loadUi('./main_elements/add_element_btn/add_element_dialog.ui', self)  # load ui

        # set a name of window
        self.setWindowTitle("Создание нового элемента")

        # save the category_id
        self.category_id = category_id

        # get the default color from db
        category_data = db.get_category_by_id(self.category_id)
        self.backcolor = category_data[2]
        self.textcolor = category_data[3]
        self.bordercolor = category_data[4]

        # get the default backgrounds for labels
        self.backcolor_label.setStyleSheet(f'background-color: {self.backcolor}')
        self.textcolor_label.setStyleSheet(f'background-color: {self.textcolor}')
        self.bordercolor_label.setStyleSheet(f'background-color: {self.bordercolor}')

        self.initUI()

    def initUI(self):
        # element_name_edit for name of element
        self.element_name_edit.setPlaceholderText('Введите название элемента')

        # set placeholder to description
        self.description_edit.setPlaceholderText('Вот тут введите описание категории')

        # every btn
        self.backcolor_btn.clicked.connect(
            self.back_color_pick
        )
        self.textcolor_btn.clicked.connect(
            self.text_color_pick
        )
        self.bordercolor_btn.clicked.connect(
            self.border_color_pick
        )

        # ok button working
        self.ok_btn.clicked.connect(
            self.create_element
        )

    def back_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.backcolor = color.name(QColor.HexRgb)
            self.backcolor_label.setStyleSheet(
                f'background-color: {self.backcolor}'
            )

    def text_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.textcolor = color.name(QColor.HexRgb)
            self.textcolor_label.setStyleSheet(
                f'background-color: {self.textcolor}'
            )

    def border_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.bordercolor = color.name(QColor.HexRgb)
            self.bordercolor_label.setStyleSheet(
                f'background-color: {self.bordercolor}'
            )

    def create_element(self):
        ans = db.create_element_in_category(
            self.element_name_edit.text(),
            self.category_id,
            self.textcolor,
            self.backcolor,
            self.bordercolor,
            self.description_edit.toPlainText()
        )

        if ans:
            self.close()
