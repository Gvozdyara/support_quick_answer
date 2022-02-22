from tkinter import *
import os
import sqlite3


def dump_help_base():
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM sections''')
    print([row for row in cur])


def create_data_base(table_name):
    db_file_name = table_name + ".db"
    conn = sqlite3.connect(db_file_name)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS table_name(
        section_id INT PRIMARY KEY,
        section_name TEXT)''')
    conn.commit()
    # debug
    print("new table exists or created")


def add_section_to_db(section_name, ):
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()

    # make the table name where to add new sections
    table_name = "table_" + str(section_id)
    conn = sqlite3.connect("helpbase.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS table_name(
            section_id INT PRIMARY KEY,
            section_name TEXT)''')

    # start to get the last id number to add the new section to the following id
    cur.execute('''SELECT section_id FROM sections''')
    section_ids = cur.fetchall()

    # getting the las ID and add 1
    try:
        id_list = list()
        for pair in section_ids:
            id_list.append(pair[0])

        new_id = max(id_list) + 1
    except:
        new_id = 0
    query = '''INSERT INTO sections
        (section_id, section_name)
        VALUES (?, ?);'''
    values = (new_id, section_name)
    cur.execute(query, values)
    conn.commit()
    # # debug
    # dump_help_base()
    return new_id


def open_section(section_id):
    global section_frame, entry_frame
    # удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками
    for widget in section_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in entry_frame.winfo_children():
        widget.destroy()
    entry_frame.update()

    new_entry_name = "entry_" + str(section_id)
    new_entry_name = new_section_entry(new_entry_name, entry_frame)




    return


class section_btns:
    def __init__(self, frame, section_id, text, click_cmnd):
        name = "btn_" + str(section_id)
        self.name = Button(frame, text=text, command=lambda: click_cmnd(section_id))
        self.name.pack(fill=X)
        self.id = section_id




class new_section_entry:
    def __init__(self, name, frame):
        self.name = Entry(frame)
        get_entry_btn = Button(frame, text="Add section", command=lambda: add_section(self.name))

        self.name.pack(side=LEFT, expand=0)
        get_entry_btn.pack(side=RIGHT, expand=1)


def add_section(entry, ):
    global root, section_frame
    section_title = entry.get()
    section_id = add_section_to_db(section_title)
    #     for now we have unique section ID of the new section previous func
    new_section_btn = section_btns(section_frame, section_id, section_title, open_section)

        


root = Tk()
root.title("Quick respond")

create_data_base("sections")

section_frame = Frame(root)
section_frame.pack(side=BOTTOM, fill=X)

entry_frame = Frame(root)
section_entry = new_section_entry("main_section_entry", entry_frame)

root.mainloop()



        
        
