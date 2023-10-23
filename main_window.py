from PyQt5 import QtWidgets as widgets
import sys
import main_elements as ms
from PyQt5 import uic  # Импортируем uic
from db_class import db
import os


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create cache
        os.makedirs('cache', exist_ok=True)

        # load ui
        uic.loadUi('static/mainwindow.ui', self)

        # set the geometry
        self.setGeometry(0, 0, 995, 673)
        self.setWindowTitle('Films Manager')

        self.initUI()

    def initUI(self):
        # adding the button
        self.add_category_btn = ms.AddCategoryBtn(self)
        self.add_category_btn_layout.addWidget(
            self.add_category_btn
        )

        # category scroll settings
        self.category_scroll_area.setWidgetResizable(
            True
        )
        self.category_scroll_layout = widgets.QVBoxLayout(self.category_scroll_content)

        # elements scroll settings
        self.elements_scroll_area.setWidgetResizable(
            True
        )
        self.elements_scroll_layout = widgets.QVBoxLayout(self.elements_scroll_content)

        self.category_load_data()  # load data for default

        # search_btn
        self.search_line_edit.setPlaceholderText('Введите текст для поиска')
        self.search_line_edit.setToolTip('Тут вы можете удобно найти необходимую категорию')
        self.search_line_edit.textChanged.connect(
            self.category_search_data
        )

        # current_category_chosen
        self.cur_category = -1  # -1 => no category chosen

        # add element button
        self.add_element_btn.setVisible(False)  # while there no category -> hide and enable the btn
        self.add_element_btn.setEnabled(False)
        self.add_element_btn.clicked.connect(
            self.create_element
        )
        # and to a search_line_edit
        self.element_search_line_edit.setVisible(False)
        self.element_search_line_edit.setEnabled(False)
        self.element_search_line_edit.setPlaceholderText('Введите для поиска по элементам')
        self.element_search_line_edit.setToolTip('Тут вы можете удобно найти необходимый элемент')
        self.element_search_line_edit.textChanged.connect(
            self.element_search_data
        )

    def element_search_data(self):
        text = self.element_search_line_edit.text()
        elements = db.search_elements_by_category_id_text(self.cur_category, text)

        # clears all the layout
        while self.elements_scroll_layout.count():
            item = self.elements_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for element in elements:
            self.elements_scroll_layout.addWidget(
                ms.ElementBtn(self, element[0])
            )

    def category_search_data(self, text):
        # clears all the layout
        while self.category_scroll_layout.count():
            item = self.category_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # grab all data of categories
        ids = db.get_category_ids_by_search(text)
        for id in ids:
            self.category_scroll_layout.addWidget(
                ms.CategoryBtn(self, id)
            )

    def search_categories(self):
        text = self.serach_line_edit.text()
        if len(text) >= 3:
            self.category_search_data(text)

    def create_element(self):  # to another class
        ms.AddElementBtn(self, self.cur_category).create_element()

    def category_load_data(self):
        # clears all the layout
        while self.category_scroll_layout.count():
            item = self.category_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # grab all data of categories
        ids = db.get_category_ids()
        for id in ids:
            self.category_scroll_layout.addWidget(
                ms.CategoryBtn(self, id)
            )

    def elements_load_data(self, category_id: int):
        self.cur_category = category_id
        self.add_element_btn.setVisible(True)  # category selected -> visible
        self.add_element_btn.setEnabled(True)
        self.element_search_line_edit.setVisible(True)
        self.element_search_line_edit.setEnabled(True)

        elements = db.get_elements_by_category_id(category_id)

        # clears all the layout
        while self.elements_scroll_layout.count():
            item = self.elements_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for element in elements:
            self.elements_scroll_layout.addWidget(
                ms.ElementBtn(self, element[0])
            )
