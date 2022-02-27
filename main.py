from tkinter import *
import os
import sqlite3



# кнопки с именем раздела
class section_btns:
    def __init__(self, frame, section_id, text, click_cmnd, current_table, path):
        name = "btn_" + str(section_id)
        self.name = Button(frame, text=text, command=lambda: click_cmnd(section_id, current_table, text))
        self.name.pack(fill=X)
        self.id = section_id
        self.current_table = current_table
        self.text = text
        self.name.bind("<Enter>", self.on_enter)
        self.name.bind("<Leave>", self.on_leave)


    def create_inner_table_add_to_the_row(self, section_id, current_table):
        # make the table name where to add new sections
        table_name = self.text
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        create_table(cur, conn, table_name)
        #     надо добавить свеже созданую таблицу в таблицу выше уровнем в строку с section_id_var
        q = """UPDATE '{}' 
                SET section_inner_lvl = '{}'
                WHERE rowid = '{}' """
        cur.execute(q.format(current_table, table_name, section_id))
        conn.commit()


    # выводим содержимое описания к разделу (3 столбец)
    def on_enter(self, e):
        global section_inner_lvl_frame
        # чистим фрэйм
        try:
            for widget in section_inner_lvl_frame.winfo_children():
                widget.destroy()
            section_inner_lvl_frame.update()
        except:
            print("No section inner level frame to destroy")
            pass

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()

        # q = """
        #         SELECT section_inner_lvl from '{}' WHERE id = ('{}') """
        # cur.execute(q.format(self.text, self.id))
        # description = cur.fetchall()
        # print(description, " description")
        q = """SELECT section_name from '{}'"""
        cur.execute(q.format(self.text))
        to_layout_sections = ["{}\n".format(name[0]) for name in cur.fetchall()]
        to_layout_label = section_inner_lvl_label(self.text, section_inner_lvl_frame, to_layout_sections, None)
        return

    def on_leave(self, e):
        return

class new_section_entry:
    def __init__(self, name, frame, current_table, current_id):
        self.name = Entry(frame)
        get_entry_btn = Button(frame, text="Add section", command=lambda: add_section(self.name, current_table, current_id))
        self.current_id = current_id

        self.name.pack(side=LEFT, expand=0)
        get_entry_btn.pack(side=RIGHT, expand=1)


class section_inner_lvl_label:
    def __init__(self, name, frame, to_layout, current_id):
        self.name = Label(frame, wraplength=100, justify=CENTER, text=to_layout, background="RED")
        self.name.pack()



def dump_help_base(table):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    to_print = cur.execute('''SELECT * FROM "{}"'''.format(table))
    print([row for row in to_print])


# функция выкладывания кнопок текущего раздела
def layout_section_btns(current_table):
    # dump_help_base(current_table)
    global section_frame, path

    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = """SELECT rowid, section_name from '{}' """
    to_layout_list = cur.execute(q.format(current_table))
    for item in to_layout_list:
        new_section_btn = section_btns(section_frame, item[0], item[1], open_section, current_table, path)


def create_data_base(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    create_table(cur, conn, table_name)
    return table_name

# создание таблицы после подключения к базе данных
def create_table (cur, conn, table_name):
    q = '''CREATE TABLE IF NOT EXISTS "{}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_name TEXT, 
                section_inner_lvl TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()


def add_section(entry, current_table, current_id):
    global root, section_frame, path
    section_title = entry.get()
    section_id = add_section_to_db(section_title, current_table, current_id)
    #     for now we have unique section ID of the new section from the previous func
    new_section_btn = section_btns(section_frame, section_id, section_title, open_section, current_table, path)
    new_section_btn.create_inner_table_add_to_the_row(id, current_table)


def add_section_to_db(section_name_var, current_table, current_id):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = 'INSERT INTO "{}" (section_name) VALUES (?)'
    cur.execute(q.format(current_table), (section_name_var,))
    conn.commit()
    # возвращаем rowid добавленного раздела
    q = """SELECT id FROM '{}' WHERE rowid=last_insert_rowid()"""
    cur.execute(q.format(current_table))
    section_id = cur.fetchone()
    conn.commit()
    return section_id[0]


def open_section(current_id, current_table, inner_table):
    global section_frame, entry_frame, path

    # удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками
    for widget in section_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in entry_frame.winfo_children():
        widget.destroy()

    entry_frame.update()

    layout_section_btns(inner_table)

    # отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого
    new_entry_name = "entry_" + str(current_id)
    new_entry = new_section_entry(new_entry_name, entry_frame, inner_table, current_id)

    path.append((current_id, current_table, inner_table))

    back_btn.configure(command=lambda: go_to_previous_section(path))
    back_btn.update()


def go_to_previous_section(path):
    print([i for i in path], "call of go_back")

    try:
        path.pop(-1)
        print([i for i in path], " last item is poped")
    except IndexError:
        pop = Tk()
        info_message = Label(pop, text="No way back")
        OK = Button(pop, text="OK", command=lambda: pop.destroy())
        info_message.pack()
        OK.pack()
    last_path = path[-1]
    current_id = last_path[0]
    current_table = last_path[1]
    inner_table = last_path[2]

    print(current_id, "cid", current_table, "ctable",  inner_table, "itable")
    open_section(current_id, current_table, inner_table)

    print([i for i in path], "section is openned")


root = Tk()
root.title("Quick respond")
path = []


Data_base_file = "sections.db"
table_name = create_data_base(Data_base_file, "main")
section_frame = Frame(root, background="RED")
section_frame.pack(side=LEFT, fill=X)
section_inner_lvl_frame = Frame(root)
section_inner_lvl_frame.pack(side=RIGHT)

entry_frame = Frame(root)
entry_frame.pack()
section_entry = new_section_entry("main_section_entry", entry_frame, table_name, None)
layout_section_btns(table_name)

back_btn = Button(root, text="Назад", command=lambda: go_to_previous_section())
back_btn.pack()
root.mainloop()



        
        
