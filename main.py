from tkinter import *
import os
import sqlite3

# не работает не нужна
def dump_help_base():
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM sections''')
    print([row for row in cur])


def create_data_base(table_name):
    db_file_name = table_name + ".db"
    conn = sqlite3.connect(db_file_name)
    cur = conn.cursor()
    q = '''CREATE TABLE IF NOT EXISTS "{}" (id INTEGER PRIMARY KEY AUTOINCREMENT, section_name TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()
    print([row for row in cur.execute("SELECT * from {}".format(table_name))])
    # debug
    print("data base ", table_name, " created" )

    return table_name


class section_btns:
    def __init__(self, frame, section_id, text, click_cmnd):
        name = "btn_" + str(section_id)
        self.name = Button(frame, text=text, command=lambda: click_cmnd(section_id))
        self.name.pack(fill=X)
        self.id = section_id




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
    new_section_btn = section_btns(section_frame, section_id, section_title, open_section)


def add_section_to_db(section_name_var, current_table):

    conn = sqlite3.connect("main.db")
    cur = conn.cursor()
    string = cur.execute('SELECT rowid, section_name FROM "{}"'.format(current_table))
    print(string)

    q = 'INSERT INTO "{}" (section_name) VALUES (?)'

    cur.execute(q.format(current_table), (section_name_var,))
    conn.commit()
    string = cur.execute('SELECT rowid, section_name FROM "{}"'.format(current_table))
    print(string)

def open_section(section_id_var):
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
    new_entry_name = "entry_" + str(section_id)
    new_entry_name = new_section_entry(new_entry_name, entry_frame, section_id_var) #sectionid нужно добавить как rowid к вызову

    # make the table name where to add new sections
    table_name = "table_" + str(section_id_var)
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS table_name (section_id INT PRIMARY KEY section_name TEXT)")
    cur.commit()
    print([row for row in cur.execute("SELECT * FROM table_name")])
        


root = Tk()
root.title("Quick respond")

table_name = create_data_base("main")

section_frame = Frame(root, background="RED")
section_frame.pack(side=BOTTOM, fill=X)

entry_frame = Frame(root)
entry_frame.pack()
section_entry = new_section_entry("main_section_entry", entry_frame, table_name)


root.mainloop()



        
        
