from PyQt5 import QtWidgets as widgets
import sys
import main_elements as ms
from PyQt5 import uic  # Импортируем uic
from db_class import db


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # load ui
        uic.loadUi('./mainwindow.ui', self)

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

        self.category_load_data()  # load data for default

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


if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    # app.setStyleSheet('./static/style.css')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
