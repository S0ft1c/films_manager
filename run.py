from main_window import MainWindow
from PyQt5 import QtWidgets as widgets
import sys

if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)
    # app.setStyleSheet('./static/style.css')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
