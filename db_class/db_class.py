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
        bordercolor STRING,
        description TEXT
        )''')
        # id будет использоваться в другой таблице, в колонке со связкой

        # TODO: create a table for films

    def create_category(self, name: str, backcolor: str, textcolor: str,
                        bordercolor: str, desc=''):

        if not name:
            return False

        try:
            # add the data to table
            self.cursor.execute('''INSERT INTO categories 
            (name, backcolor, textcolor, bordercolor, description) VALUES 
            (?, ?, ?, ?, ?)''', (name, backcolor, textcolor, bordercolor, desc,))
            # commit data
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_category_ids(self):
        try:
            data = [el[0]
                    for el in self.cursor.execute('''select * from categories''').fetchall()
                    ]
            return data
        except Exception as e:
            print(e)
            return False

    def get_category_by_id(self, id: int):
        try:
            data = self.cursor.execute("""select * from categories where id=?""", (id,)) \
                .fetchone()
            return data
        except Exception as e:
            print(e)
            return False

    def delete_category(self, id: int):
        try:
            self.cursor.execute("""delete from categories where id=?""", (id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def edit_category(self, id: int, name: str, backcolor: str, textcolor: str,
                      bordercolor: str, desc=''):

        if not name:
            return False

        try:
            # edit the data in table
            self.cursor.execute('''update categories set
            name=?, backcolor=?, textcolor=?,
            bordercolor=?, description=? where id=?''',
                                (name, backcolor, textcolor, bordercolor, desc, id,))
            # commit data
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


db = DB()  # create an obj of class
