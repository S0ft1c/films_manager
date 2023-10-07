from PyQt5 import QtWidgets as widgets
from db_class import db
from PyQt5.QtGui import QIcon
from .edit_category_dialog import EditCategoryDialog
from PyQt5.QtCore import Qt


class CategoryBtn(widgets.QLabel):
    def __init__(self, s, id: int):
        super().__init__(s)

        self.s = s
        self.id = id

        self.setFixedHeight(100)  # here is a fixed height of label

        # get data from db
        data = db.get_category_by_id(id)
        if not data:
            raise BaseException(f"no data for {id}- category")
        else:
            self.name = data[1]
            self.backcolor = data[2]
            self.textcolor = data[3]
            self.bordercolor = data[4]
            self.desc = data[5]

        # create a texts
        self.setText(self.name)
        self.setToolTip(self.desc)

        self.setStyleSheet('QLabel {' + f"""border: 4px solid {self.bordercolor};
        text-color: {self.textcolor};
        background-color: {self.backcolor};
        border-radius: 5px;
        font-family: 'Lato', sans-serif;
        font-weight: 500;
        font-size: 24;
        padding-left: 25px;""" + '}')

        # context menu
        self.menu = widgets.QMenu(self.s)

        # edit action
        self.edit_action = widgets.QAction('Редактировать', self)
        self.edit_action.triggered.connect(self.edit_category)
        self.menu.addAction(self.edit_action)

        # del action
        self.del_action = widgets.QAction('Удалить', self)
        self.del_action.triggered.connect(self.delete_category)
        self.menu.addAction(self.del_action)

        # place a politics for label
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # connect the mousePressEvent
        self.mousePressEvent = self.left_click

    def left_click(self, event):
        if event.button() == Qt.LeftButton:
            self.s.elements_load_data(self.id)

    def show_context_menu(self, event):
        # Отображаем контекстное меню в указанной позиции
        self.menu.exec_(self.mapToGlobal(event))

    def delete_category(self):  # delete category
        if not db.delete_category(self.id):
            pass

    def edit_category(self):
        label = self.sender().parentWidget()  # receive for what label it was
        layout = label.parentWidget().layout()  # what layout it is
        if layout is not None:  # here ew can find the index in layout
            index = layout.indexOf(label)
        else:
            return False

        # get the needed id by index of layout
        id = db.get_category_ids()[index]

        dialog = EditCategoryDialog(id=id)
        dialog.exec_()
