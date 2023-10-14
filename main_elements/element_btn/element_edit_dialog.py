from PyQt5 import QtWidgets as widgets
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
                index, value = widget.return_data().split('-')
                self.data[database_indexes_dictionary[index]] = value

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
            pass

    def add_uniq_info(self):
        if self.uniq_info_combobox.currentText() == 'Последняя серия':
            # if user want to add series
            if self.data[6] is None:  # and there no series
                self.data[6] = '0, 0'
                self.load_uniq_info()  # load the info
