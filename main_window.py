from PyQt5 import QtWidgets as widgets
import sys
import main_elements as ms
from PyQt5 import uic  # Импортируем uic
from db_class import db


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.category_load_btn.clicked.connect(
            self.category_load_data
        )

        # elements scroll settings
        self.elements_scroll_area.setWidgetResizable(
            True
        )
        self.elements_scroll_layout = widgets.QVBoxLayout(self.elements_scroll_content)

        # self.elements_load_btn.clicked.connect(  TODO: create an update btn
        #     self.category_load_data
        # )

        self.category_load_data()  # load data for default

        # current_category_chosen
        self.cur_category = -1  # -1 => no category chosen

        # add element button
        self.add_element_btn.setVisible(False)  # while there no category -> hide and enable the btn
        self.add_element_btn.setEnabled(False)
        self.add_element_btn.clicked.connect(
            self.create_element
        )

    def create_element(self):  # to another class
        ms.AddElementBtn(self.cur_category).create_element()

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
