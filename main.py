from tkinter import *
import os
import sqlite3

# не работает не нужна
def dump_help_base():
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM sections''')
    print([row for row in cur])


def create_data_base(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    create_table(cur, conn, table_name)
    return table_name


def create_table (cur, conn, table_name):
    q = '''CREATE TABLE IF NOT EXISTS "{}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_name TEXT, 
                section_inner_lvl TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()
    return table_name

class section_btns:
    def __init__(self, frame, section_id, text, click_cmnd, current_table):
        name = "btn_" + str(section_id)
        self.name = Button(frame, text=text, command=lambda: click_cmnd(section_id, current_table))
        self.name.pack(fill=X)
        self.id = section_id
        self.current_table = current_table

    def create_inner_table_add_to_the_row(self, section_id, current_table):
        # make the table name where to add new sections
        table_name = "table_" + str(section_id)
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        table = create_table(cur, conn, table_name)
        #     надо добавить свеже созданую таблицу в таблицу выше уровнем в строку с section_id_var
        q = """UPDATE '{}' 
                SET section_inner_lvl = '{}'
                WHERE rowid = '{}' """
        cur.execute(q.format(current_table, table, section_id))
        print("Inner table is nested")


class new_section_entry:
    def __init__(self, name, frame, current_table):
        self.name = Entry(frame)
        get_entry_btn = Button(frame, text="Add section", command=lambda: add_section(self.name, current_table))

        self.name.pack(side=LEFT, expand=0)
        get_entry_btn.pack(side=RIGHT, expand=1)




def add_section(entry, current_table):
    global root, section_frame
    section_title = entry.get()
    section_id = add_section_to_db(section_title, current_table)
    #     for now we have unique section ID of the new section from the previous func
    new_section_btn = section_btns(section_frame, section_id, section_title, open_section, current_table)
    new_section_btn.create_inner_table_add_to_the_row(id, current_table)


def add_section_to_db(section_name_var, current_table):

    conn = sqlite3.connect("main.db")
    cur = conn.cursor()
    string = cur.execute('SELECT rowid, section_name FROM "{}"'.format(current_table))
    print(string)

    q = 'INSERT INTO "{}" (section_name) VALUES (?)'

    cur.execute(q.format(current_table), (section_name_var,))
    conn.commit()
    # возвращаем rowid добавленного раздела
    q = """SELECT rowid FROM '{}'"""
    section_id = cur.execute(q.format(current_table))
    return section_id

def open_section(section_id_var, current_table):
    global section_frame, entry_frame
    # удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками
    for widget in section_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in entry_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого
    new_entry_name = "entry_" + str(section_id_var)
    new_entry = new_section_entry(new_entry_name, entry_frame) # sectionid нужно добавить как rowid к вызову


root = Tk()
root.title("Quick respond")

Data_base_file = "sections.db"
table_name = create_data_base(Data_base_file, "main")

section_frame = Frame(root, background="RED")
section_frame.pack(side=BOTTOM, fill=X)

entry_frame = Frame(root)
entry_frame.pack()
section_entry = new_section_entry("main_section_entry", entry_frame, table_name)


root.mainloop()



        
        
