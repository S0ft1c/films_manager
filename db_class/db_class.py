import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('base.sqlite3')
        self.cursor = self.conn.cursor()

        # creating the table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name STRING,
        backcolor STRING,
        textcolor STRING,
        description TEXT
        )''')
        # id будет использоваться в другой таблице, в колонке со связкой

        # TODO: create a table for films

    def create_category(self, name: str, backcolor: str, textcolor: str, desc=''):

        if not name:
            return False

        try:
            # add the data to table
            self.cursor.execute('''INSERT INTO categories 
            (name, backcolor, textcolor, description) VALUES 
            (?, ?, ?, ?)''', (name, backcolor, textcolor, desc,))
            # commit data
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


db = DB()  # create an obj of class
