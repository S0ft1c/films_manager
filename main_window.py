from PyQt5 import QtWidgets as widgets
import sys
import main_elements as ms
import db_class


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # set the geometry
        self.setGeometry(0, 0, 800, 800)
        self.setWindowTitle('Task1')

        self.initUI()

    def initUI(self):
        self.add_category_btn = ms.AddCategoryBtn(self)
        self.add_category_btn.move(10, 10)


if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    # app.setStyleSheet('./static/style.css')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
