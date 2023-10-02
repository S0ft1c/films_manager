from PyQt5 import QtWidgets as widgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5 import uic  # Импортируем uic
from db_class import db

ok_btn_style = """color: #fff;
  border-radius: 5px;
  padding: 10px 25px;
  font-family: 'Lato', sans-serif;
  font-weight: 500;
  background-color: #4dccc6;
  background-image: linear-gradient(315deg, #4dccc6 0%, #96e4df 74%);
  line-height: 42px;
  padding: 0;
"""

change_color_style = """color: #fff;
  border-radius: 5px;
  padding: 10px 25px;
  font-family: 'Lato', sans-serif;
  font-weight: 500;
  background-color: #6495ED;
"""

result_label_style = """
border: 4px solid #484848;
border-radius: 2px;
text-align: center;
font-size: 16px;
font-wight: bold;"""


class EditCategoryDialog(widgets.QDialog):
    def __init__(self, id):
        super().__init__()

        self.id = id  # needed id for editing

        # подгружаем дизайн
        uic.loadUi("./main_elements/add_category_btn/add_category_dialog.ui", self)

        # set a name of window
        self.setWindowTitle("Создание собственной категории")

        # all of this is for fucking animation
        self.text = "Редактируйте пока можете (хехе)"
        self.current_text = ''
        self.index = 0
        self.is_typing = True  # Флаг для определения написан ли текст
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(100)  # Задержка между символами (миллисекунды)

        self.initUI()

    def initUI(self):

        # line_edit for name of category
        self.line_edit.setPlaceholderText('Введите тут название вашей категории')
        # при каждом изменении текста, все будет идти в "пример"
        self.line_edit.textChanged.connect(
            self.text_changed
        )

        # result label
        self.result_label.setStyleSheet(result_label_style)

        # btn for backcolor
        self.backcolor_btn.setStyleSheet(change_color_style)
        self.backcolor_btn.clicked.connect(self.back_color_pick)

        # backcolor var
        self.backcolor = "#FFFFFF"  # white

        # btn for textcolor
        self.textcolor_btn.setStyleSheet(change_color_style)
        self.textcolor_btn.clicked.connect(self.text_color_pick)

        # textcolor var
        self.textcolor = "#000000"  # white

        # border var
        self.bordercolor = "#484848"  # grey

        # border color
        self.border_btn.setStyleSheet(change_color_style)
        self.border_btn.clicked.connect(
            self.border_color_pick
        )

        # description_text
        self.description_text.setPlaceholderText('Введите тут описание категории...')

        # btn OK
        self.ok_btn.setStyleSheet(ok_btn_style)
        self.ok_btn.clicked.connect(self.add_to_db)  # add to db the variant

    def border_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.bordercolor = color.name(QColor.HexRgb)
            self.border_label.setStyleSheet(
                f'background-color: {self.bordercolor};'  # set a new color
            )
            self.result_label.setStyleSheet(
                self.result_label.styleSheet() +
                f'border: 4px solid {self.bordercolor};'  # set a new color of back to result
            )

    def update_text(self):
        if self.is_typing:
            if self.index < len(self.text):
                self.current_text += self.text[self.index]
                self.label.setText(self.current_text + '|')
                self.index += 1
            else:
                self.is_typing = False  # Текст напечатан, переключаем флаг

        else:
            if len(self.current_text) > 0:
                self.current_text = self.current_text[:-1]  # Удаляем последний символ
                self.label.setText(self.current_text + "|")
            else:
                self.is_typing = True  # Весь текст стерт, переключаем флаг
                self.index = 0

    def back_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.backcolor = color.name(QColor.HexRgb)
            self.backcolor_label.setStyleSheet(
                f'background-color: {self.backcolor};'  # set a new color
            )
            self.result_label.setStyleSheet(
                self.result_label.styleSheet() +
                f'background-color: {self.backcolor};'  # set a new color of back to result
            )

    def text_color_pick(self):
        color = widgets.QColorDialog.getColor()
        if color.isValid():
            self.textcolor = color.name(QColor.HexRgb)
            self.textcolor_label.setStyleSheet(
                f'background-color: {self.textcolor};'  # set a new color
            )
            self.result_label.setStyleSheet(
                self.result_label.styleSheet() +
                f'color: {self.textcolor};'  # set a new color of text to result
            )

    def text_changed(self):
        self.result_label.setText(
            self.line_edit.text()
        )

    def add_to_db(self):

        ans = db.edit_category(
            name=self.line_edit.text(),
            textcolor=self.textcolor,
            backcolor=self.backcolor,
            bordercolor=self.bordercolor,
            desc=self.description_text.toPlainText(),
            id=self.id,
        )

        if ans:
            self.close()
