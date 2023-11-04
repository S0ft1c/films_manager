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

        self.cursor.execute('''create table if not exists elements (
        id INTEGER PRIMARY KEY,
        name string,
        category_id integer,
        textcolor string,
        backcolor string,
        bordercolor string,
        last_series string,
        last_page string,
        link string,
        file_path string,
        description text
        )''')

    def search_elements_by_category_id_text(self, category_id, text):
        try:
            els = self.cursor.execute('''select * from elements where category_id=?''',
                                       (category_id,)).fetchall()
            ans = []
            for el in els:
                if text in el[1]:
                    ans.append(el)
            return ans
        except Exception as e:
            print(e)
            return False

    def get_category_ids_by_search(self, text):
        try:
            ans = []
            data = self.cursor.execute("""select * from categories""").fetchall()
            for el in data:
                if text in el[1]:
                    ans.append(el[0])
            return ans
        except Exception as e:
            print(e)
            return []

    def delete_element(self, id):
        try:
            self.cursor.execute("""delete from elements where id=?""", (id,))
            self.conn.commit()
            return True
        except Exception as e:
            return False

    def get_element_by_id(self, id: int):
        try:
            data = self.cursor.execute('''select * from elements where id=?''',
                                       (id,)).fetchone()
            return data
        except Exception as e:
            print(e)
            return []

    def create_element_in_category(self, name: str, category_id: int, textcolor: str, backcolor: str,
                                   bordercolor: str, desc: str):
        if not name:
            return False

        try:
            self.cursor.execute('''insert into elements (name, category_id, textcolor, backcolor,
            bordercolor, description) values (?, ?, ?, ?, ?, ?)''',
                                (name, category_id, textcolor, backcolor, bordercolor, desc,))
            self.conn.commit()
            return True
        except Exception as e:
            return False

    def get_elements_by_category_id(self, category_id: int):
        try:
            return self.cursor.execute('''select * from elements where category_id=?''',
                                       (category_id,)).fetchall()
        except Exception as e:
            return False

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
            self.cursor.execute("""delete from categories where id=?""",
                                (id,))
            self.conn.commit()
            self.cursor.execute("""delete from elements where category_id=?""",
                                (id,))
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

    def edit_element(self, id: int, data: list):
        try:
            self.cursor.execute('''update elements set name=?, last_series=?, last_page=?, link=?,
            file_path=?, description=? where id=?''',
                                (data[1], data[6], data[7], data[8], data[9], data[10],
                                 id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


db = DB()  # create an obj of class
