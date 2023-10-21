from PyQt5 import QtWidgets as widgets
from PyQt5.QtWidgets import QFileDialog
import shutil
from db_class import db
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5 import uic  # Импортируем uic
import main_elements.element_btn.uniq_info as uniq_info

# this dictionary needed for the edit_element foo
database_indexes_dictionary = {
    'last_series': 6,
    'last_page': 7,
    'web': 8,
    'file': 9,
}


class EditElementDialog(widgets.QDialog):
    def __init__(self, s, id):
        super().__init__()

        self.id = id
        self.s = s

        uic.loadUi('static/element_edit_dialog.ui', self)
        self.setWindowTitle("Редактирование элемента")
        self.data = list(db.get_element_by_id(id))

        self.initUI()

    def initUI(self):

        # set the name and desc
        self.name_line_edit.setText(self.data[1])
        self.description_plain_text_edit.setPlainText(self.data[10])

        # change the text in the name and desc
        self.name_line_edit.textChanged.connect(self.name_changed)
        self.description_plain_text_edit.textChanged.connect(self.desc_changed)

        # add elements to combobox
        self.uniq_info_combobox.addItem('Последняя серия')
        self.uniq_info_combobox.setItemData(0, 'Добавление последней серии / сезона', Qt.ToolTipRole)
        self.uniq_info_combobox.addItem('Последняя страница')
        self.uniq_info_combobox.setItemData(1, 'Если это книга, добавьте закладку', Qt.ToolTipRole)
        self.uniq_info_combobox.addItem('Ссылка на веб-ресурс')
        self.uniq_info_combobox.setItemData(2, 'Добавьте ссылку на сайт', Qt.ToolTipRole)
        self.uniq_info_combobox.addItem('Добавить файл')
        self.uniq_info_combobox.setItemData(3, 'Вы выберите файл, и он отобразится тут.'
                                               ' После можно удалять. Он уже тут.', Qt.ToolTipRole)

        # connect the add_uniq_info_btn
        self.add_uniq_info_btn.clicked.connect(self.add_uniq_info)

        # layouts
        self.uniq_info_scroll_layout = widgets.QVBoxLayout(self.uniq_info_scroll_content)

        # change btn
        self.change_btn.clicked.connect(self.edit_data)

        # default load uniq data
        self.load_uniq_info()

    def desc_changed(self):
        self.data[10] = self.description_plain_text_edit.toPlainText()

    def name_changed(self):
        self.data[1] = self.name_line_edit.text()

    def edit_data(self):  # edit the element (for the last button)
        while self.uniq_info_scroll_layout.count():  # iter in the layout
            item = self.uniq_info_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                index, value = widget.return_data().split('|')
                if database_indexes_dictionary[index] != 9:  # if it's not a file
                    self.data[database_indexes_dictionary[index]] = value
        self.data[9] = None if not self.data[9] else self.data[9]  # if it's '', we need to change to None

        if db.edit_element(self.id, self.data):
            self.s.s.elements_load_data(self.s.category_id)  # all of this is for auto-update!
            self.close()

    def load_uniq_info(self):
        # clears all the layout
        while self.uniq_info_scroll_layout.count():
            item = self.uniq_info_scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if self.data[6] is not None:
            last_s_widget = uniq_info.LastSeriesWidget(self, self.data[6])
            self.uniq_info_scroll_layout.addWidget(last_s_widget)
            last_s_widget.show()

        if self.data[7] is not None:
            last_p_widget = uniq_info.LastPageWidget(self, self.data[7])
            self.uniq_info_scroll_layout.addWidget(last_p_widget)
            last_p_widget.show()

        if self.data[8] is not None:
            web_widget = uniq_info.WebWidget(self, self.data[8])
            self.uniq_info_scroll_layout.addWidget(web_widget)
            web_widget.show()

        if self.data[9] is not None:
            for file in self.data[9].split(', '):
                file_widget = uniq_info.FileWidget(self, file)
                self.uniq_info_scroll_layout.addWidget(file_widget)
                file_widget.show()

    def add_uniq_info(self):

        if self.uniq_info_combobox.currentText() == 'Последняя серия':
            # if user want to add series
            if self.data[6] is None:  # and there no series
                self.data[6] = '0, 0'
                self.load_uniq_info()  # load the info

        if self.uniq_info_combobox.currentText() == 'Последняя страница':
            # if user want to add page
            if self.data[7] is None:  # and there no pages
                self.data[7] = '0'
                self.load_uniq_info()

        if self.uniq_info_combobox.currentText() == 'Ссылка на веб-ресурс':
            # if user want to add the web page
            if self.data[8] is None:
                self.data[8] = 'Пусто тут'
                self.load_uniq_info()

        if self.uniq_info_combobox.currentText() == 'Добавить файл':
            # if user want to add the another file
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName()
            if file_path:
                # we need our new filepath: 'cache/<smth>'
                new_file_path = f'cache/{file_path.split("/")[-1]}'
                if self.data[9]:
                    self.data[9] = ', '.join(self.data[9].split(', ') + [new_file_path])
                else:
                    self.data[9] = ', '.join([new_file_path])
                # copy file to a cache
                shutil.copy2(file_path, new_file_path)
                self.load_uniq_info()
